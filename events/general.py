from discord.ext import commands

import random

emojis = [ '\U0001F602', '\U0000261D', '\U0001F44D', '\U0001F44E' ]

class GeneralEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

def setup(bot):
    bot.add_cog(GeneralEvents(bot))