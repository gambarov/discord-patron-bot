from dataclasses import dataclass

from discord import user
from . import config
from discord.ext.commands.converter import EmojiConverter

@dataclass
class GamePlayer():
    user: config.UserType
    emoji: str