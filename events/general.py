import discord, random
from discord.ext import commands

class GeneralEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("🕵️ Дело"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not message.content.startswith(self.bot.command_prefix):
            command = self.bot.get_cog('ChatCommand')
            return await command.execute(message)
                

def setup(bot):
    bot.add_cog(GeneralEvents(bot))