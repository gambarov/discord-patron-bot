import random
from commands.chat.manager import ChatDatabaseManager
from discord.ext import commands

class ChatCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = ChatDatabaseManager()

    async def execute(self, message):
        answers = self.manager.find(message.content, 0.75)
        answer = random.choice(answers)
        if answer:
            await message.channel.send(answer['text'])

def setup(bot):
    bot.add_cog(ChatCommand(bot))