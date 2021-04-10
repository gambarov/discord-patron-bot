from discord.ext import commands

class GeneralEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

def setup(bot):
    bot.add_cog(GeneralEvents(bot))