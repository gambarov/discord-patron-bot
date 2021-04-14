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
        if isinstance(message.channel, discord.TextChannel):
            if random.randrange(0, 100) <= 10 or self.bot.user.mentioned_in(message):
                command = self.bot.get_cog('ChatCommand')
                return await command.execute(message)

def setup(bot):
    bot.add_cog(GeneralEvents(bot))