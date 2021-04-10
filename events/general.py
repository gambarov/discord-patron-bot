from utils.helper import get_error_embed
from discord.ext import commands

class GeneralEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=get_error_embed(desc="Слишком частый вызов команды, попробуйте позже"))

def setup(bot):
    bot.add_cog(GeneralEvents(bot))