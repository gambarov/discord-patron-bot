from discord.ext import commands
import logging

emojis = [ '\U0001F602', '\U0000261D', '\U0001F44D', '\U0001F44E' ]

logger = logging.getLogger('discord')

class GeneralEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Connected to Discord")

def setup(bot):
    bot.add_cog(GeneralEvents(bot))