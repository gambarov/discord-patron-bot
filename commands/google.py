import os, requests, json

from discord.ext import commands

class GoogleDictCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "гугл", help = "получение значений определения")
    async def execute(self, context, *, text):
        response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/ru/{}'.format(text))
        print(response.text)
        json_data = json.loads(response.text)
        await context.send(self.get_definition(json_data))
    
    def get_definition(self, data):
        if not isinstance(data, list):
            return 'ничего не найдено'

        data = data[0]

        if not 'meanings' in data:
            return 'ничего не найдено'

        return '{}: {}'.format(data['word'], data['meanings'][0]['definitions'][0]['definition'])


def setup(bot):
    bot.add_cog(GoogleDictCommand(bot))