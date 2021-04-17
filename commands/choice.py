import random

from discord.ext import commands

class ChoiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "выбери", help = "выбор случайного варианта (ввод через 'или')")
    async def execute(self, context, *, variants):
        texts = [ "Определенно,", "Думаю, что", "Вероятно,", "Скорее всего,", "" ]
        variants = [ variant.strip() for variant in variants.split(' или ') ]
        variant = random.choice(variants)
        await context.send('{} {}'.format(random.choice(texts), variant))

    @execute.error
    async def info_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await context.send("Введите варианты через 'или'")

def setup(bot):
    bot.add_cog(ChoiceCommand(bot))