import random

from discord.ext import commands

class ChoiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "выбери", help = "выбор случайного варианта")
    async def execute(self, context, *variants):
        # Если не из чего выбирать
        if len(variants) == 0:
            return

        texts = [ "Лучше", "Думаю, что", "Вероятно," ]
        variant = random.choice(variants)
        await context.send('{} {}'.format(random.choice(texts), variant))

def setup(bot):
    bot.add_cog(ChoiceCommand(bot))

