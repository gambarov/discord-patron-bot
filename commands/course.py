import aiohttp
import json

import discord
from discord.ext import commands

class CourseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_chars = [ 'EUR', 'USD' ]
        
    @commands.command(name = "курс", help = "текущий курс валют")
    async def execute(self, context, *, chars=None):
        chars = self.default_chars if chars == None else chars.split()
        embed = discord.Embed(colour = 0x4299F5)
        courses = await self.get_courses()
        # Перебираем все валюты
        for code, data in courses.items():
            for need in chars:
                # Если попалась с нужным кодом
                if code == need.upper():
                    nominal = data['Nominal'] if int(data['Nominal']) > 1 else ''
                    name  = data['Name']
                    value = round(data['Value'], 2)
                    diff  = round(data['Value'] - data['Previous'], 2)
                    diff  = '+{}'.format(diff) if diff >= 0 else diff
                    embed.add_field(
                        name = '{} {}'.format(nominal, name),
                        value = '{} ₽ ({})'.format(value, diff),
                        inline=True
                    )

        embed.add_field(
            name='Биткоин',
            value='{} $'.format(await self.get_bitcoin_cost()),
            inline=True
        )

        await context.send(embed = embed)

    @staticmethod
    async def get_courses():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.cbr-xml-daily.ru/daily_json.js") as response:
                if response.status == 200:
                    return json.loads(await response.text())['Valute']

    @staticmethod
    async def get_bitcoin_cost(valute='USD'):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://blockchain.info/ticker") as response:
                if response.status == 200:
                    return json.loads(await response.text())[valute]['buy']

def setup(bot):
    bot.add_cog(CourseCommand(bot))