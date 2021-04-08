import logging
from discord.ext.commands import Bot
from utils import files
from bot.config import options, PRIVATE

logger = logging.getLogger('discord')

class Patron(Bot):
    def __init__(self):
        super().__init__(**options)
        self._load_extensions('commands')
        self._load_extensions('events')
        self.load_extension('commands.market.command')
        self.load_extension('commands.tictactoe.command')
        self.add_check(self.is_private_mode)

    def _load_extensions(self, system):
        for file in files.get_py_files(system):
            self.load_extension('{}.{}'.format(system.replace('/', '.'), file))

    # TODO:
    # async def on_error(self, event_method, *args, **kwargs):
    #     return super().on_error(event_method, *args, **kwargs)

    def is_private_mode(self, ctx):
        if PRIVATE:
            return ctx.author.id == 627833817708625931
        return True