import logging
from discord.ext.commands import Bot
from utils import files
from bot.config import options

logger = logging.getLogger('discord')

class Patron(Bot):
    def __init__(self):
        super().__init__(**options)
        self._load_extensions('commands')
        self._load_extensions('events')
        self.load_extension('commands.exchange.command')

    def _load_extensions(self, system):
        for file in files.get_py_files(system):
            self.load_extension('{}.{}'.format(system.replace('/', '.'), file))