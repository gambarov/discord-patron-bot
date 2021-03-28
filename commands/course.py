from discord import colour
import requests
import json

import discord
from discord.ext import commands

class CourseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_chars = [ 'EUR', 'USD' ]
        
    @commands.command(name = "курс", help = "текущий курс валют")
    async def execute(self, context, *, chars=None):
        # Получаем данные
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        json_data = json.loads(response.text)

        message = 'Курс валют:' + '\n'

        chars = self.default_chars if chars == None else chars.split()
        embed = discord.Embed(colour = 0x4299F5)

        # Перебираем все валюты
        for code, data in json_data['Valute'].items():
            # Если попалась с нужным кодом
            for need in chars:
                if code == need.upper():
                    name  = data['Name']
                    value = round(data['Value'], 2)
                    diff  = round(data['Value'] - data['Previous'], 2)
                    diff  = '+{}'.format(diff) if diff >= 0 else diff
                    embed.add_field(
                        name = name,
                        value = '{} ₽ ({})'.format(value, diff),
                        inline=True
                    )

        # Курс биткоина
        bitcoin_cost = self.get_bitcoin_cost()

        embed.add_field(
            name='Биткоин',
            value='{} $'.format(bitcoin_cost),
            inline=True
        )

        await context.send(embed = embed)

    @staticmethod
    def get_bitcoin_cost(valute='USD'):
        response = requests.get('https://blockchain.info/ticker')
        return json.loads(response.text)[valute]['buy']

def setup(bot):
    bot.add_cog(CourseCommand(bot))