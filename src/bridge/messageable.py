from __main__ import Harmony
from typing import Union, Optional
from user import User

class Messageable:
    def __init__(self, bridge, is_room, can_message=True):
        self.__bridge: Harmony = bridge
        self.__is_room = is_room
        self.__can_message = can_message
        self.user: Optional[User] = None

    @property
    def can_message(self):
        return self.__can_message

    @property
    def is_room(self):
        return self.__is_room

    async def send(self, content, user: Union[User, dict] = None, specials: dict = None):
        if not self.__can_message:
            raise ValueError("cannot message this destination")

        if self.__is_room:
            await self.__bridge.send_bridge(self, content, user, specials)
        else:
            await self.__bridge.send_bot(self, content, specials)
