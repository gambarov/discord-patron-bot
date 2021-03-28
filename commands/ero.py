import discord
from discord.ext import commands

import io, os
import aiohttp

import random

from bs4 import BeautifulSoup

class EroCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ero", help = "some ero")
    async def execute(self, ctx, *, tag='pussy'):

        image_id = await self._get_random_image_id(tag)
        url = await self._get_image_url(image_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                if response.status != 200:
                    raise Exception('Could\'nt download file')
                
                data = io.BytesIO(await response.read())
                await ctx.send(file=discord.File(data, '{}.png'.format(tag), spoiler=True))

    @execute.error
    async def info_error(self, ctx, error):
        print(error)
        return await ctx.send('Не получилось получить фото')

    async def _get_random_image_id(self, tag):
        page = random.choice(range(1, await self._get_max_page(tag)))
        response = await self._get_response_text('https://erowall.com/teg/{}/page/{}'.format(tag, page))
        ids = []
        soup = BeautifulSoup(markup=response, features="html.parser") 
        content = soup.find('div', { 'class':'content'} )
        wpminis = content.find_all('div', { 'class':'wpmini' } )

        for wpmini in wpminis:
            a = wpmini.find('a')
            if a:
                img = a.find('img')
                if img:
                    url = img.get('src')                
                    id = url.rsplit('/', 1)[-1]     # split url and get last (name.jpg)
                    id = os.path.splitext(id)[0]    # remove ext (.jpg)
                    ids.append(id)

        return random.choice(ids)

    async def _get_image_url(self, id):
        response = await self._get_response_text('https://erowall.com/w/{}/'.format(id))
        soup = BeautifulSoup(markup=response, features="html.parser") 
        viewwallpaper = soup.find('div', { 'class':'viewwallpaper'} )

        if viewwallpaper:
            a = viewwallpaper.find('a', { 'class':'img' })
            if a:
                img = a.find('img')
                if img:
                    url = img.get('src')
                    return 'https://erowall.com/' + url 
        return None

    async def _get_max_page(self, tag):
        markup = await self._get_response_text('https://erowall.com/search/{}/'.format(tag))
        soup = BeautifulSoup(markup=markup, features="html.parser") 
        paginator = soup.find('div', { 'class':'paginator' })
        ul = paginator.find('ul')
        num = 1
        for li in ul.find_all('li'):
            try:
                num = int(li.find('a').string)
            except:
                pass
        print(num)
        return num

    async def _get_response_text(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return ''
                await session.close()
                return await response.text()
        return ''

def setup(bot):
    bot.add_cog(EroCommand(bot))