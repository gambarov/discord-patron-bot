import os, json
import aiohttp

from discord.ext import commands

KEY = os.getenv('WEATHER_KEY')

class WeatherCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "http://api.weatherapi.com/v1/current.json"

    @commands.command(name = "погода", help = "в представлении не нуждается")
    async def execute(self, context, *, city):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, data = { 'key':KEY, 'lang':'ru', 'q':city }) as response:
                if response.status != 200:
                    return await context.send("Не могу получить данные")
                data = json.loads(await response.text())
                await context.send(self.parse(data))
    
    @execute.error
    async def info_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await context.send("Укажите город")

        print('{}: {}'.format(type(error), error))
        await context.send("Не удалось получить погоду")

    def parse(self, data):
        if (not 'location' in data) or (len(data['current']) == 0):
            return "Данные отсутствуют, попробуйте позже" 

        location = data['location']
        current = data['current']
        message = '{} ({}, {}): \n' .format(location['name'], location['region'], location['country'])
        message += "Температура: {} ℃, {} \n".format(current['temp_c'], current['condition']['text'])
        message += "Чувствуется как: {} ℃ \n".format(current['feelslike_c'])
        return message

def setup(bot):
    bot.add_cog(WeatherCommand(bot))