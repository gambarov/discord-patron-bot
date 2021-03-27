import os, requests, json

from discord.ext import commands

KEY = os.getenv('WEATHER_KEY')

class WeatherCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "погода", help = "в представлении не нуждается")
    async def execute(self, context, *, city):
        response = requests.post('http://api.weatherapi.com/v1/current.json', data = { 'key':KEY, 'lang':'ru', 'q':city })
        print(response.text)

        if response.status_code != 200:
            return await context.send('Не могу получить погоду по данному городу')

        json_data = json.loads(response.text)
        await context.send(self.get_message(json_data))
    
    def get_message(self, data):
        if not 'location' in data:
            return 'Ошибка№1, попробуйте еще раз позже' 

        location = data['location']
        current = data['current']
        message = '{} ({}, {}): \n' .format(location['name'], location['region'], location['country'])
        message += 'Температура: {} ℃, {} \n'.format(current['temp_c'], current['condition']['text'])
        message += 'Чувствуется как: {} ℃ \n'.format(current['feelslike_c'])
        return message

def setup(bot):
    bot.add_cog(WeatherCommand(bot))