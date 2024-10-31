from messageable import Messageable

class RoomPrivateMeta:
    def __init__(self, server, allowed, invites, platform):
        self.__server = server
        self.__allowed = allowed
        self.__invites = invites
        self.__platform = platform

    @property
    def server(self):
        """Owner server's ID"""
        return self.__server

    @property
    def owner(self):
        """Alias to RoomPrivateMeta.server"""
        return self.__server

    @property
    def allowed(self):
        """Servers with access to the Private Room"""
        return self.__allowed

    @property
    def invites(self):
        """Private Room invites"""
        return self.__invites

    @property
    def platform(self):
        """Owner server's origin platform"""
        return self.__platform


class Room(Messageable):
    def __init__(
            self, bridge, name, description, display_name, emoji, servers, private, restricted, locked, rules, banned
    ):
        super().__init__(bridge, True)
        self.__bridge = bridge
        self.__name = name
        self.__description = description
        self.__display_name = display_name
        self.__emoji = emoji
        self.__servers = servers
        self.__private = private
        self.__restricted = restricted
        self.__locked = locked
        self.__rules = rules
        self.__banned = banned
        self.__private_meta = RoomPrivateMeta(None, [], [], 'discord')

    @property
    def _room_template(self):
        """Base dict object to represent a room."""
        return {
            'rules': [], 'restricted': False, 'locked': False, 'private': False,
            'private_meta': {
                'server': None,
                'allowed': [],
                'invites': [],
                'platform': 'discord'
            },
            'emoji': None, 'description': None, 'display_name': None, 'banned': []
        }

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def display_name(self):
        return self.__display_name

    @property
    def emoji(self):
        return self.__emoji

    @property
    def servers(self):
        return self.__servers

    @property
    def private(self):
        return self.__private

    @property
    def restricted(self):
        return self.__restricted

    @property
    def locked(self):
        return self.__locked

    @property
    def rules(self):
        return self.__rules

    @property
    def banned(self):
        return self.__banned

    @property
    def private_meta(self):
        return self.__private_meta

    def get_platform_servers(self, platform):
        return self.__servers[platform]

    # noinspection PyTypeChecker
    def to_dict(self):
        template = dict(self._room_template)

        template['meta']['name'] = self.__name
        template['meta']['description'] = self.__description
        template['meta']['display_name'] = self.__display_name
        template['meta']['emoji'] = self.__emoji
        template['meta']['private'] = self.__private

        template['meta']['private_meta']['server'] = self.__private_meta.server
        template['meta']['private_meta']['allowed'] = self.__private_meta.allowed
        template['meta']['private_meta']['invites'] = self.__private_meta.invites
        template['meta']['private_meta']['platform'] = self.__private_meta.platform

        template.update(self.__servers)

        return template
