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

class WebhookCacheStore:
    def __init__(self, bot):
        self.__bot = bot
        self.__webhooks = {}

    def store_webhook(self, webhook, identifier, server):
        if not server in self.__webhooks.keys():
            self.__webhooks.update({server: {identifier: webhook}})
        self.__webhooks[server].update({identifier: webhook})
        return len(self.__webhooks[server])

    def store_webhooks(self, webhooks: list, identifiers: list, servers: list):
        if not len(webhooks) == len(identifiers) == len(servers):
            raise ValueError('webhooks, identifiers, and servers must be the same length')

        for index in range(len(webhooks)):
            webhook = webhooks[index]
            identifier = identifiers[index]
            server = servers[index]
            if not server in self.__webhooks.keys():
                self.__webhooks.update({server: {identifier: webhook}})
            self.__webhooks[server].update({identifier: webhook})
        return len(self.__webhooks)

    def get_webhooks(self, server: int or str):
        try:
            server = int(server)
        except:
            pass
        if len(self.__webhooks[server].values())==0:
            raise ValueError('no webhooks')
        return list(self.__webhooks[server].values())

    def get_webhook(self, identifier: int or str):
        try:
            identifier = int(identifier)
        except:
            pass
        for guild in self.__webhooks.keys():
            if identifier in self.__webhooks[guild].keys():
                return self.__webhooks[guild][identifier]
        raise ValueError('invalid webhook')

    def clear(self, server: int or str = None):
        if not server:
            self.__webhooks = {}
        else:
            self.__webhooks[server] = {}
        return
