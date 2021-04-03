import discord, logging
from discord.ext import commands

import io, os
import aiohttp

import random

from bs4 import BeautifulSoup

from utils.checks import is_vip_user
from utils.helper import get_discord_color

logger = logging.getLogger('discord')

class EroCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = {}

    @commands.command(name = "ero", help = "some ero")
    @commands.check_any(commands.is_owner(), is_vip_user())
    async def execute(self, ctx, *, tag='pussy'):
        async with ctx.typing():
            image_id = await self.parse_random_image_id(tag)
            url = await self.parse_image_url(image_id)

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
            return await ctx.send(embed = discord.Embed(title = "Доступ ограничен", description = "Команда доступна только для VIP-пользователей", colour = get_discord_color('error')))
        logger.exception(error)
        await ctx.send(embed = discord.Embed(description = "Не удалось получить фото", colour = get_discord_color('error')))

    async def parse_random_image_id(self, tag):
        page = random.choice(range(1, await self.parse_max_page(tag) + 1))
        response = await self.get_response_text("https://erowall.com/teg/{}/page/{}".format(tag, page))
        soup = BeautifulSoup(markup = response, features = "html.parser") 
        content = soup.find('div', { 'class':'content'} )
        wpminis = content.find_all('div', { 'class':'wpmini' } )
        ids = []

        for wpmini in wpminis:
            a = wpmini.find('a')
            if a:
                img = a.find('img')
                if img:
                    img_id = img.get('src').rsplit('/', 1)[-1]  # split url and get last (id.jpg)
                    img_id = os.path.splitext(img_id)[0]            # remove ext (id)
                    ids.append(img_id)
        return random.choice(ids)

    async def parse_image_url(self, img_id):
        response = await self.get_response_text('https://erowall.com/w/{}/'.format(img_id))
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

    async def parse_max_page(self, tag):
        try:
            num = self.tags[tag]['max_page']
            return num
        except:
            pass

        soup = BeautifulSoup(
            markup = await self.get_response_text("https://erowall.com/search/{}/".format(tag)), 
            features = "html.parser") 
        paginator = soup.find('div', { 'class':'paginator' })
        ul = paginator.find('ul')
        num = 1
        for li in ul.find_all('li'):
            try:
                num = int(li.find('a').string)
            except:
                pass
        # Кешируем данные
        self.tags[tag] = { 'max_page':num }
        return num

    async def get_response_text(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return ''
                await session.close()
                return await response.text()

def setup(bot):
    bot.add_cog(EroCommand(bot))