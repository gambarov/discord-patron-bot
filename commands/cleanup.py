from discord.ext import commands

class CleanupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "уборка", help = "удаление сообщений, связанных с командами бота")
    async def execute(self, context, *, limit=10):
        limit = min(limit, 50)
        channel = context.message.channel

        target_messages = []
        history_messages = await channel.history(limit=limit).flatten()

        for message in history_messages:
            # Любое сообщение, отправленное ботом
            if message.author == self.bot.user:
                target_messages.append(message)
                continue
            # Если сообщение начинается с вызова какой-либо команды
            for command in self.bot.commands:
                if message.content.startswith('{}{}'.format(self.bot.command_prefix, command.name)):
                    target_messages.append(message)

        await channel.delete_messages(target_messages)

def setup(bot):
    bot.add_cog(CleanupCommand(bot))