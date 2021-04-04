import discord, random
from utils.helper import get_discord_color, get_error_embed
from discord.ext import commands

class KnifeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "нож", help = "открытие кейсов")
    async def execute(self, context, count = 10):
        knifes = 0
        count = min(count, 1000000)
        for i in range(0, count):
            if self.possibly():
                knifes += 1

        embed = discord.Embed(title = "📢 Результат", description = "Вы открыли {} 📦 и получили {} 🗡️!".format(str(count), str(knifes)), colour = get_discord_color('info'))
        await context.send(embed = embed)

    @execute.error
    async def on_error(self, context, error):
        if (isinstance(error, commands.BadArgument)):
            await context.send(embed = get_error_embed(desc = "Аргумент должен быть числом"))
        await context.send(embed = get_error_embed(desc = "Не получилось открыть кейсы"))

    def possibly(self):
        return random.randrange(1, 10001) <= 25

def setup(bot):
    bot.add_cog(KnifeCommand(bot))