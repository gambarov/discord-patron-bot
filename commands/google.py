import discord, aiohttp, json

from discord.ext import commands
from utils.helper import get_discord_color

class GoogleDictCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "гугл", help = "получение значений определения")
    async def execute(self, context, *, text):
        async with context.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.dictionaryapi.dev/api/v2/entries/ru/{}'.format(text)) as response:
                    if response.status != 200:
                        return await context.send(embed = discord.Embed(description = "Не удалось получить определение", colour = get_discord_color('error')))
                    json_data = json.loads(await response.text())
                    await context.send(self.parse_definition(json_data))
    
    def parse_definition(self, data):
        if not isinstance(data, list):
            return 'Ничего не найдено'

        data = data[0]

        if not 'meanings' in data:
            return 'Ничего не найдено'

        return '{}: {}'.format(data['word'], data['meanings'][0]['definitions'][0]['definition'])


def setup(bot):
    bot.add_cog(GoogleDictCommand(bot))