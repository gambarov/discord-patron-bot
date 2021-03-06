import discord, logging
from discord.ext import commands
from utils.helper import get_discord_color, get_error_embed
from commands.course import CourseCommand

logger = logging.getLogger(__name__)

class ConvertCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "con", help = "конвертирование валют")
    async def execute(self, ctx, amount: int, from_valute: str, to_valute:str):
        courses = await CourseCommand.get_courses()
        courses['RUB'] = { 'CharCode':'RUB', 'Value':1, 'Nominal':1 }
        courses['BTC'] = { 'CharCode':'BTC', 'Value':await CourseCommand.get_bitcoin_cost('RUB'), 'Nominal':1 }
        
        from_valute = from_valute.upper()
        to_valute = to_valute.upper()        

        if not from_valute in courses:
            return await ctx.send(embed = get_error_embed(desc = "Валюта '{}' не существует".format(from_valute)))
        if not to_valute in courses:
            return await ctx.send(embed = get_error_embed(desc = "Валюта '{}' не существует".format(to_valute)))
        
        from_course = courses[from_valute]
        to_course = courses[to_valute]

        result = (amount * (int(from_course['Value']) / int(from_course['Nominal']))) / int((to_course['Value']) / int(to_course['Nominal']))
        result = round(result, 2)
        embed = discord.Embed(title = "Результат:", description = "{} {}".format(result, to_valute), colour = get_discord_color('success'))
        await ctx.send(embed = embed)

    @execute.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description = "!con [кол-во] [из валюты] [в валюту]", colour = get_discord_color('info'))
            embed.set_author(name = "Помощь")
            embed.add_field(name = "Пример", value = "!con 1000 rub usd", inline=False)
            return await ctx.send(embed = embed)
        if isinstance(error, commands.BadArgument):
            return await ctx.send(embed = get_error_embed(desc = "Некорректный ввод"))
        logger.exception(error)

def setup(bot):
    bot.add_cog(ConvertCommand(bot))