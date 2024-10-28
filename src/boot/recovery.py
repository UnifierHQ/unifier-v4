"""
Unifier - A sophisticated Discord bot uniting servers and platforms
Copyright (C) 2024  Green, ItsAsheer

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

import traceback
import tomli
import sys

try:
    sys.path.insert(0, '.')
    from src.utils import secrets
except:
    print('\x1b[31;1mSomething went wrong.\x1b[0m')
    sys.exit(1)


with open('config.toml', 'rb') as file:
    # noinspection PyTypeChecker
    config = tomli.load(file)

def command_help():
    print('\x1b[36;1mCommands:\x1b[0m')
    for command in commands:
        print(f'\x1b[36m{command}\x1b[0m')

def diagnose():
    """Diagnoses common Unifier issues."""

    # Step 1: check dependencies


commands = {
    'help': command_help,
    'exit': lambda: sys.exit(0)
}

print('Type "help" for a list of commands.')

while True:
    try:
        command = input('> ').lower()
    except KeyboardInterrupt:
        break

    try:
        commands[command]()
    except KeyError:
        print('\x1b[33;1mInvalid command. Type "help" for a list of commands.\x1b[0m')
    except KeyboardInterrupt:
        pass
    except:
        traceback.print_exc()
        print('\x1b[31;1mAn error occurred.\x1b[0m')
