class Host:
    """A public interface for safely interacting with a platform's bot object."""

    def __init__(self, bridge, host, platform):
        self.__host = host
        self.__platform = platform
        self.__platform_support = bridge.platforms.get_platform(platform)

    @property
    def platform(self):
        return self.__platform

    @property
    def id(self):
        return self.__platform_support.bot_id()

    @property
    def name(self):
        return self.__platform_support.bot_name()

    @property
    def discriminator(self):
        try:
            return self.__platform_support.bot_discriminator()
        except:
            return None

    @property
    def display_name(self):
        try:
            return self.__platform_support.bot_display_name() or self.__platform_support.bot_name()
        except:
            return self.__platform_support.bot_name()

    async def execute(self, *args, **kwargs):
        """Executes a function on the asyncio executor."""
        return await self.__platform_support.execute(*args, **kwargs)
