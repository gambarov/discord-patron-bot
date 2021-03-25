import os, requests, json

from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv('WEATHER_KEY')

from discord.ext import commands

class UrbanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = 'https://mashape-community-urban-dictionary.p.rapidapi.com/define'

    @commands.command(name = "ud", help = "urban dictionary")
    async def execute(self, context, *, term):

        headers = {
            'x-rapidapi-key': KEY,
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }

        response = requests.request('GET', self.api, headers = { 'x-rapidapi-key':KEY }, params = {"term":term})
        print('UrbanCommand: response code: {}'.format(response.status_code))
        print(response.text)
        json_data = json.loads(response.text)

        if len(json_data['list']) != 0:
            item = json_data['list'][0]
            message = '{}\n{}\n{}'.format(item['definition'], item['example'], '[1/{}]'.format(len(json_data['list'])))
            await context.send(message)
        else:
            await context.send('no definitions')

def setup(bot):
    bot.add_cog(UrbanCommand(bot))