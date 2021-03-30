import discord
from discord.ext import commands

import io, os
import aiohttp

import random

from bs4 import BeautifulSoup

from utils.checks import is_cartel
from utils.helper import get_discord_color

class EroCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ero", help = "some ero")
    @commands.check_any(commands.is_owner(), is_cartel())
    async def execute(self, ctx, *, tag='pussy'):
        image_id = await self._parse_random_image_id(tag)
        url = await self._parse_image_url(image_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception('Could\'nt download file')
                
                data = io.BytesIO(await response.read())
                await ctx.send(file = discord.File(data, '{}.png'.format(tag), spoiler = True))

    @execute.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, AttributeError):
                return await ctx.send(embed = discord.Embed(description = "Такого раздела не существует", colour = get_discord_color('error')))
        if isinstance(error, commands.CheckFailure):
            return await ctx.send(embed = discord.Embed(description = "Команда доступна только для членов сервера Manada Gaming", colour = get_discord_color('error')))
        print(type(error), error)
        await ctx.send("Не удалось получить фото")

    async def _parse_random_image_id(self, tag):
        page = random.choice(range(1, await self._parse_max_page(tag)))
        response = await self._get_response_text("https://erowall.com/teg/{}/page/{}".format(tag, page))
        soup = BeautifulSoup(markup=response, features="html.parser") 
        content = soup.find('div', { 'class':'content'} )
        wpminis = content.find_all('div', { 'class':'wpmini' } )

        ids = []

        for wpmini in wpminis:
            a = wpmini.find('a')
            if a:
                img = a.find('img')
                if img:
                    id = img.get('src').rsplit('/', 1)[-1]  # split url and get last (id.jpg)
                    id = os.path.splitext(id)[0]            # remove ext (id)
                    ids.append(id)
        return random.choice(ids)

    async def _parse_image_url(self, id):
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

    async def _parse_max_page(self, tag):
        soup = BeautifulSoup(
            markup = await self._get_response_text("https://erowall.com/search/{}/".format(tag)), 
            features = "html.parser") 
        paginator = soup.find('div', { 'class':'paginator' })
        ul = paginator.find('ul')
        num = 1
        for li in ul.find_all('li'):
            try:
                num = int(li.find('a').string)
            except:
                pass
        return num

    async def _get_response_text(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return ''
                await session.close()
                return await response.text()

def setup(bot):
    bot.add_cog(EroCommand(bot))