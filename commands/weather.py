import os, json
from utils.helper import get_discord_color
import aiohttp

import discord, logging
from discord.ext import commands

logger = logging.getLogger('discord')

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
                    return await context.send(embed = discord.Embed(description = "Не могу получить данные", colour = get_discord_color('error')))
                data = json.loads(await response.text())
                await context.send(embed = self.parse_to_embed(data))
    
    @execute.error
    async def info_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await context.send("Укажите город")
        logger.exception(error)
        await context.send(embed = discord.Embed(description = "Не удалось получить погоду", colour = get_discord_color('error')))

    def parse_to_embed(self, data):
        if (not 'location' in data) or (len(data['current']) == 0):
            return discord.Embed(description = "Данные отсутствуют, попробуйте позже", colour = get_discord_color('error'))

        location = data['location']
        current = data['current']
        embed = discord.Embed(title = "Локация", description = '{} ({}, {})'.format(location['name'], location['region'], location['country']), colour = get_discord_color('info'))
        embed.add_field(name = "Температура", value = "{} ℃, {}".format(current['temp_c'], current['condition']['text']))
        embed.add_field(name = "Чувствуется как", value = "{} ℃".format(current['feelslike_c']))
        return embed

def setup(bot):
    bot.add_cog(WeatherCommand(bot))