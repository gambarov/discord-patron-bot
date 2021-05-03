import random
import discord
import asyncio
import logging
from events.chat.manager import ChatDatabaseManager
from discord.ext import commands

from config import PRIVATE

logger = logging.getLogger(__name__)


class ChatEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = ChatDatabaseManager()
        self.reply_chance = 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.should(message):
            return

        answers = self.manager.find(message.content, 0.6)
        if not answers:
            return
        answer = random.choice(answers)['text']

        async with message.channel.typing():
            await asyncio.sleep(2)
            if isinstance(message.channel, discord.TextChannel):
                await message.reply(answer)
            else:
                await message.channel.send(answer)

    def should(self, message):
        if message.author == self.bot.user:
            return False
        if PRIVATE:
            return False
        if not message.content.startswith(self.bot.command_prefix):
            return (random.randint(1, 100) <= self.reply_chance or isinstance(message.channel, discord.DMChannel))

    async def cog_command_error(self, ctx, error):
        if isinstance(error, discord.HTTPException):
            return
        logger.exception(error)


def setup(bot):
    bot.add_cog(ChatEvent(bot))
