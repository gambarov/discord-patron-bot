from discord.ext import commands

class GeneralEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        print('{}: {}'.format(message.author, message.content))

def setup(bot):
    bot.add_cog(GeneralEvents(bot))