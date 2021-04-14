import random

import discord, asyncio 
from commands.chat.manager import ChatDatabaseManager
from discord.ext import commands

class ChatCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = ChatDatabaseManager()

    async def execute(self, message):
        if not self.should(message):
            return

        answers = self.manager.find(message.content, 0.7)
        if not answers:
            return
        answer = random.choice(answers)['text']
            
        async with message.channel.typing():
            await asyncio.sleep(1)
            if isinstance(message.channel, discord.TextChannel):
                await message.reply(answer)
            else:
                await message.channel.send(answer)

    def should(self, message):
        return random.randrange(0, 100) <= 10 or self.bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel)

def setup(bot):
    bot.add_cog(ChatCommand(bot))