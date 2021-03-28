import os, requests, json

from discord.ext import commands

import discord
import aiohttp, io

KEY = os.getenv('UNSPLASH_KEY')

class GirlCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "girl", help = "girl")
    async def execute(self, context):
        response = requests.get('https://api.unsplash.com/photos/random?query=female&client_id={}&content_filter=high'.format(KEY))
        print(response.text)

        if response.status_code != 200:
            return await context.send('Не могу получить фото в данный момент (№1)')

        data = json.loads(response.text)

        if 'urls' in data:
            url = data['urls']['regular']

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:

                    if response.status != 200:
                        return await context.send('Could\'nt download file...')
                    
                    data = io.BytesIO(await response.read())
                    return await context.send(file=discord.File(data, 'girl.png'))

        return await context.send('Не могу получить фото в данный момент (№2)')


def setup(bot):
    bot.add_cog(GirlCommand(bot))