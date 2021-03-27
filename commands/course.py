import requests
import json

from discord.ext import commands
from requests.models import Response

class CourseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.need_courses = [ 'CAD', 'EUR', 'USD' ]
        
    @commands.command(name = "курс", help = "текущий курс валют")
    async def execute(self, context):
        # Получаем данные
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        json_data = json.loads(response.text)

        message = 'Курс валют:' + '\n'

        # Перебираем все валюты
        for code, data in json_data['Valute'].items():
            # Если попалась с нужным кодом
            for need in self.need_courses:
                if code == need:
                    name  = data['Name']
                    value = round(data['Value'], 2)
                    diff  = round(data['Value'] - data['Previous'], 2)
                    diff  = '+{}'.format(diff) if diff >= 0 else diff
                    message += "{}: {} ({})".format(name, value, diff) + '\n'

        # Курс биткоина
        bitcoin_cost = self.get_bitcoin_cost()
        message += 'Биткоин: {}$'.format(bitcoin_cost)

        await context.send(message)

    @staticmethod
    def get_bitcoin_cost(valute='USD'):
        response = requests.get('https://blockchain.info/ticker')
        return json.loads(response.text)[valute]['buy']


def setup(bot):
    bot.add_cog(CourseCommand(bot))