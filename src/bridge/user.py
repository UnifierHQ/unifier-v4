from messageable import Messageable
from typing import Union

class Permissions:
    def __init__(self, **kwargs):
        self.__read_messages = kwargs.get("read_messages", False)
        self.__send_messages = kwargs.get("send_messages", False)
        self.__manage_messages = kwargs.get("manage_messages", False)
        self.__kick_members = kwargs.get("kick_members", False)
        self.__ban_members = kwargs.get("ban_members", False)
        self.__manage_channels = kwargs.get("manage_channels", False)
        self.__manage_server = kwargs.get("manage_server", False)

    @property
    def read_messages(self):
        return self.__read_messages

    @property
    def send_messages(self):
        return self.__send_messages

    @property
    def manage_messages(self):
        return self.__manage_messages

    @property
    def kick_members(self):
        return self.__kick_members

    @property
    def ban_members(self):
        return self.__ban_members

    @property
    def manage_channels(self):
        return self.__manage_channels

    @property
    def manage_server(self):
        return self.__manage_server


class User(Messageable):
    def __init__(
            self, bridge, user_id: Union[int, str], username: str = None, discriminator: str = "0",
            display_name: str = None
    ):
        super().__init__(bridge, False)
        self.__id = user_id
        self.__username = username
        self.__display_name = display_name
        self.__discriminator = discriminator

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def display_name(self):
        # user's display name is either their display name or their username
        return self.__display_name or self.__username

    @property
    def discriminator(self):
        return self.__discriminator

    def __str__(self):
        return f'{self.username}#{self.discriminator}'

class SystemUser(User):
    def __init__(self, bridge):
        super().__init__(bridge, bridge.host.id, bridge.host.name, bridge.host.discriminator, bridge.host.display_name)
        self.__can_message = False
