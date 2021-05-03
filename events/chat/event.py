import random
import discord
import asyncio
from events.chat.manager import ChatDatabaseManager
from discord.ext import commands

from utils.checks import is_test_channel
from config import PRIVATE

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
            return (random.randint(1, 100) <= self.reply_chance or self.bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel))


def setup(bot):
    bot.add_cog(ChatEvent(bot))
