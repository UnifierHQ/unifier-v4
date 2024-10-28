"""
Unifier - A sophisticated Discord bot uniting servers and platforms
Copyright (C) 2023-present  UnifierHQ

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import json
import base64
import traceback
import string
from dotenv import load_dotenv
from Crypto.Random import random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto import Random as CryptoRandom

# import ujson if installed
try:
    import ujson as json  # pylint: disable=import-error
except:
    pass

class Encryptor:
    def __init__(self):
        pass

    def encrypt(self, encoded, password):
        """Encrypts a given bytes object."""
        salt = CryptoRandom.get_random_bytes(16)
        __key = PBKDF2(password, salt, dkLen=32)

        nonce = CryptoRandom.get_random_bytes(12)
        __cipher = AES.new(__key, AES.MODE_GCM, nonce=nonce)
        result, tag = __cipher.encrypt_and_digest(encoded)
        del __key
        del __cipher
        return result, base64.b64encode(tag).decode('ascii'), base64.b64encode(nonce).decode('ascii'), base64.b64encode(salt).decode('ascii')

    def decrypt(self, encrypted, password, tag_string, salt_string, nonce_string):
        """Decrypts a given encrypted bytes object."""
        nonce = base64.b64decode(nonce_string)
        tag = base64.b64decode(tag_string)
        salt = base64.b64decode(salt_string)
        __key = PBKDF2(password, salt, dkLen=32)
        __cipher = AES.new(__key, AES.MODE_GCM, nonce=nonce)
        result = __cipher.decrypt_and_verify(encrypted, tag)
        del __key
        del __cipher
        return result

class TokenStore:
    def __init__(self, encrypted, password=None, salt=None, debug=False, content_override=None, onetime=None):
        self.__is_encrypted = encrypted
        self.__encryptor = Encryptor()
        self.__password = password
        self.__one_time = onetime or []
        self.__accessed = []

        if encrypted:
            if not password:
                raise ValueError('encryption password must be provided')
            if not salt:
                raise ValueError('encryption salt must be provided')

            # file is in json format
            try:
                with open('secrets/.encryptedenv', 'r') as file:
                    self.__data: dict = json.load(file)
            except:
                self.__data: dict = {}
        else:
            # file is in dotenv format, load using load_dotenv
            # we will not encapsulate dotenv data for the sake of backwards compatibility
            if content_override:
                # content override is a feature only to be used by bootloader
                self.__data: dict = content_override
            else:
                load_dotenv()
                self.__data: dict = dict(os.environ)

        self.__debug = debug

    @property
    def encrypted(self):
        return self.__is_encrypted

    @property
    def debug(self):
        return self.__debug

    @property
    def tokens(self):
        if not self.__is_encrypted:
            raise ValueError('cannot retrieve keys when tokens are unencrypted')

        tokens = list(self.__data.keys())
        tokens.remove('test')
        return tokens

    @property
    def accessed(self):
        return self.__accessed

    def to_encrypted(self, password):
        dotenv = open('.env', 'r')
        lines = dotenv.readlines()
        dotenv.close()

        keys = []
        for line in lines:
            key = line.split('=', 1)[0]
            while key.endswith(' '):
                key = key[:-1]
            keys.append(key)

        encrypted_env = {'test': None}

        test_value, test_tag, test_nonce, test_salt = self.__encryptor.encrypt(str.encode(
            ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(16)])
        ), password)

        encrypted_env['test'] = {
            "ciphertext": base64.b64encode(test_value).decode('ascii'),
            "tag": test_tag,
            "nonce": test_nonce,
            "salt": test_salt
        }

        # we can get values from dotenv, since that's been done if TokenStore is not encrypted

        for key in keys:
            __token = os.environ.get(key)
            if not __token:
                continue

            encrypted_value, tag, nonce, salt = self.__encryptor.encrypt(str.encode(__token), password)
            encrypted_env.update({key: {
                "ciphertext": base64.b64encode(encrypted_value).decode('ascii'),
                "tag": tag,
                "nonce": nonce,
                "salt": salt
            }})
            del os.environ[key]

        with open('secrets/.encryptedenv', 'w+') as file:
            # noinspection PyTypeChecker
            json.dump(encrypted_env, file)

        self.__data = encrypted_env
        self.__password = password
        self.__is_encrypted = True

    def test_decrypt(self, password=None):
        if not self.__is_encrypted:
            return True

        try:
            self.__encryptor.decrypt(
                base64.b64decode(self.__data['test']['ciphertext']),
                password or self.__password,
                self.__data['test']['tag'],
                self.__data['test']['salt'],
                self.__data['test']['nonce']
            )
        except:
            if self.__debug:
                traceback.print_exc()

            return False
        return True

    def retrieve(self, identifier):
        if identifier in self.__one_time:
            if identifier in self.__accessed:
                raise ValueError('token has already been retrieved')
            self.__accessed.append(identifier)
        data = str.encode(self.__data[identifier]['ciphertext'])
        nonce = self.__data[identifier]['nonce']
        tag = self.__data[identifier]['tag']
        salt = self.__data[identifier]['salt']
        decrypted = self.__encryptor.decrypt(
            base64.b64decode(data),
            self.__password,
            tag,
            salt,
            nonce
        )
        return decrypted.decode('utf-8')

    def add_token(self, identifier, token):
        if identifier in self.__data.keys():
            raise KeyError('token already exists')

        encrypted, tag, nonce, salt = self.__encryptor.encrypt(str.encode(token), self.__password)
        self.__data.update({identifier: {
            'ciphertext': base64.b64encode(encrypted).decode('ascii'),
            "tag": tag,
            "nonce": nonce,
            "salt": salt
        }})
        self.save('secrets/.encryptedenv')
        return len(self.__data)

    def replace_token(self, identifier, token, password):
        # password prompt to prevent unauthorized token deletion
        if not self.test_decrypt(password=password):
            raise ValueError('invalid password')

        if not identifier in self.tokens:
            raise KeyError('token does not exist')

        if identifier == 'test':
            raise ValueError('cannot replace token, this is needed for password verification')

        encrypted, tag, nonce, salt = self.__encryptor.encrypt(str.encode(token), self.__password)
        self.__data.update({identifier: {
            'ciphertext': base64.b64encode(encrypted).decode('ascii'),
            'tag': tag,
            'nonce': nonce,
            'salt': salt
        }})
        self.save('secrets/.encryptedenv')

    def delete_token(self, identifier, password):
        # password prompt to prevent unauthorized token deletion
        if not self.test_decrypt(password=password):
            raise ValueError('invalid password')

        if not identifier in self.tokens:
            raise KeyError('token does not exist')

        if identifier == 'test':
            raise ValueError('cannot delete token, this is needed for password verification')

        del self.__data[identifier]
        self.save('secrets/.encryptedenv')
        return len(self.__data)

    def reencrypt(self, current_password, password):
        if not self.test_decrypt(password=current_password):
            raise ValueError('invalid password')

        for key in self.__data.keys():
            token = self.retrieve(key)
            encrypted, tag, nonce, salt = self.__encryptor.encrypt(str.encode(token), password)
            self.__data[key] = {
                'ciphertext': base64.b64encode(encrypted).decode('ascii'),
                'tag': tag,
                'nonce': nonce,
                'salt': salt
            }

        self.__password = password
        self.save('secrets/.encryptedenv')

    def save(self, filename):
        if not self.__is_encrypted:
            raise ValueError('cannot save unencrypted data')

        test_value, test_tag, test_nonce, test_salt = self.__encryptor.encrypt(str.encode(
            ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(16)])
        ), self.__password)

        self.__data.update({'test': {
            'ciphertext': base64.b64encode(test_value).decode('ascii'),
            'tag': test_tag,
            'nonce': test_nonce,
            'salt': test_salt
        }})

        with open(filename, 'w+') as file:
            # noinspection PyTypeChecker
            json.dump(self.__data, file)
