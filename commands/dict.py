import os, requests, json

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('YANDEX_DICT_TOKEN')

from discord.ext import commands

class DictyonaryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'

    @commands.command(name = "что", help = "получение подробных словарных статей")
    async def execute(self, context, *, text):
        response = requests.post(self.api, data = { 'key':TOKEN, 'lang':'ru-ru', 'text':text })
        print(response.text)
        json_data = json.loads(response.text)
        await context.send('{}: {}'.format(text, self.get_message(json_data)))

    def get_message(self, data):
        if len(data['def']) == 0:
            return 'такого слова нет в словаре'

        tr = data['def'][0]['tr']
        message = ''

        for t in tr:
            text = t['text']
            message += text

            if 'syn' in t:
                syns = t['syn']
                for syn in syns:
                    message += ' | {}'.format(syn['text'])

            if tr[-1] is not t: message += ', '

        return message

def setup(bot):
    bot.add_cog(DictyonaryCommand(bot))