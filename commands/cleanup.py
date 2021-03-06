from discord.ext import commands
import logging
import utils.helper

logger = logging.getLogger(__name__)

class CleanupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "очистка", help = "удаление сообщений, связанных с командами бота")
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.channel)
    @commands.guild_only()
    async def execute(self, context, limit=10):
        limit = min(limit, 100)
        channel = context.message.channel

        def is_trash_message(message):
            if message.author == self.bot.user:
                return True
            # Если сообщение начинается с вызова какой-либо команды
            for command in self.bot.commands:
                if message.content.startswith('{}{}'.format(self.bot.command_prefix, command.name)):
                    return True
            return False
        
        await channel.purge(limit = limit, check = is_trash_message)

    @execute.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(embed = utils.helper.get_error_embed(desc = "Команда предназначена только для серверов"))

def setup(bot):
    bot.add_cog(CleanupCommand(bot))