import discord
from discord.ext import commands
from utils import checks, helper

class GeneralEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("Дело 🕵️"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        if isinstance(error, checks.PremiumRequired):
            return await ctx.send(embed=discord.Embed(title="⛔ Доступ ограничен", description="Команда доступна только для VIP-пользователей", colour=helper.get_discord_color('error')))
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=helper.get_error_embed(desc="Слишком частый вызов команды, попробуйте позже"))

def setup(bot):
    bot.add_cog(GeneralEvents(bot))