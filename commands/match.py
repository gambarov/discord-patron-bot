import os, json, discord, logging, aiohttp
from utils.helper import get_discord_color, get_error_embed
from discord.ext import commands

logger = logging.getLogger('discord')

KEY = os.getenv('URBAN_KEY')
API_URL = "https://love-calculator.p.rapidapi.com/getPercentage"

class LoveMatchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "love", help = "любовная совместимость")
    async def execute(self, context, *, names):
        names = [ name.strip() for name in names.split(' and ') ]
        if len(names) <= 1:
            return await context.send(embed = get_error_embed(desc = "??"))
        name1 = self.format_name(names[0])
        name2 = self.format_name(names[1])

        params = { "fname":name1, "sname":name2 }
        logging.debug(params)
        headers = {
            'x-rapidapi-key': KEY,
            'x-rapidapi-host': "love-calculator.p.rapidapi.com",
        }

        async with context.typing():
            async with aiohttp.ClientSession() as session:
                async with session.request("GET", url = API_URL, params = params, headers = headers) as response:
                    if response.status != 200:
                        logging.error(await response.text())
                        raise Exception()

                    data = json.loads(await response.text())
                    logging.debug(data)
                    percentage = data['percentage'] if 'percentage' in data else None

                    if not percentage:
                        raise Exception()

                    embed = discord.Embed(
                        title = "👥 {} и {}".format(name1, name2), 
                        description = "✨ Совместимость: {}% {}".format(str(percentage), self.get_emoji(int(percentage))), 
                        colour = get_discord_color('info'))
                    await context.send(embed = embed)

    def format_name(self, name):
        if name.lower() == "я":
            return 'Ты'
        return name.title()

    def get_emoji(self, percent):
        if percent < 40:
            return '💔'
        elif percent >= 40 and percent < 70:
            return '❤️'
        else:
            return '💖'

    @execute.error
    async def on_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await context.send("Введите имена через 'и'")
        logger.exception(error)
        await context.send(embed = get_error_embed(desc = "Не удалось получить данные"))

def setup(bot):
    bot.add_cog(LoveMatchCommand(bot))