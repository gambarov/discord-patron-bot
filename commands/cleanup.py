from discord.ext import commands

class CleanupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "уборка", help = "удаление сообщений, связанных с командами бота")
    async def execute(self, context):
        channel = context.message.channel

        target_messages = []
        history_messages = await channel.history(limit=15).flatten()

        for message in history_messages:
            if message.author == self.bot.user:
                print('Message to delete: ' + message.content)
                target_messages.append(message)
                continue

            for command in self.bot.commands:
                if message.content.startswith('{}{}'.format(self.bot.command_prefix, command.name)):
                    print('Message to delete: ' + message.content)
                    target_messages.append(message)

        await channel.delete_messages(target_messages)
        
            

def setup(bot):
    bot.add_cog(CleanupCommand(bot))