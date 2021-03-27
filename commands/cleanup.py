from discord.ext import commands

class CleanupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "уборка", help = "удаление сообщений, связанных с командами бота")
    async def execute(self, context, *count):
        channel = context.message.channel

        target_messages = []
        history_messages = await channel.history(limit=10).flatten()

        for message in history_messages:
            # Сообщение, отправленное ботом
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