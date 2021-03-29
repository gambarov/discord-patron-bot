import random
from re import split

from discord.ext import commands

class ChoiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "выбери", help = "выбор случайного варианта (ввод через запятую)")
    async def execute(self, context, *, variants):
        texts = [ "Лучше", "Думаю, что", "Вероятно," ]
        variants = [ variant.strip() for variant in variants.split(',') ]
        variant = random.choice(variants)
        await context.send('{} {}'.format(random.choice(texts), variant))

    @execute.error
    async def info_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await context.send("Введите варианты через запятую")
        
        print("{}: {}".format(type(error), error))
        await context.send("Не удалось выбрать вариант")

def setup(bot):
    bot.add_cog(ChoiceCommand(bot))

