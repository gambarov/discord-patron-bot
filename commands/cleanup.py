from discord.ext import commands
import logging

logger = logging.getLogger('discord')

class CleanupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "уборка", help = "удаление сообщений, связанных с командами бота")
    async def execute(self, context, *, limit=10):
        limit = min(limit, 50)
        channel = context.message.channel
        await channel.delete_messages(await self.get_trash_messages(channel, limit))

    async def cog_command_error(self, ctx, error):
        logger.exception(error)
        await ctx.send("Не удалось провести уборку")

    async def get_trash_messages(self, channel, limit):
        messages = []
        async for message in channel.history(limit=limit):
            # Любое сообщение, отправленное ботом
            if message.author == self.bot.user:
                messages.append(message)
                continue
            # Если сообщение начинается с вызова какой-либо команды
            for command in self.bot.commands:
                if message.content.startswith('{}{}'.format(self.bot.command_prefix, command.name)):
                    messages.append(message)
        return messages

def setup(bot):
    bot.add_cog(CleanupCommand(bot))