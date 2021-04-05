import discord, logging
from discord.ext import commands

import io, os
import aiohttp

import random

from bs4 import BeautifulSoup

from utils.checks import is_vip_user
from utils.helper import get_discord_color, get_error_embed

logger = logging.getLogger('discord')

class EroCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = {}

    @commands.command(name = "ero", help = "some ero")
    @commands.check_any(commands.is_owner(), is_vip_user())
    async def execute(self, ctx, *, tag = ''):
        async with ctx.typing():
            img_id = str(random.randrange(1, 32000)) if not tag else await self.parse_random_image_id(tag)
            url = await self.parse_image_url(img_id)

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception('Could\'nt download file')
                    
                    data = io.BytesIO(await response.read())
                    await ctx.send(file = discord.File(data, '{}.png'.format(tag if tag else 'ero'), spoiler = False))

    @execute.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, AttributeError):
                return await ctx.send(embed = get_error_embed(desc = "Такого раздела не существует"))
        if isinstance(error, commands.CheckFailure):
            return await ctx.send(embed = discord.Embed(title = "⛔ Доступ ограничен", description = "Команда доступна только для VIP-пользователей", colour = get_discord_color('error')))
        logger.exception(error)
        await ctx.send(embed = get_error_embed(desc = "Не удалось получить фото"))

    async def parse_random_image_id(self, tag):
        page = random.choice(range(1, await self.parse_max_page(tag) + 1))
        response = await self.get_response_text("https://erowall.com/teg/{}/page/{}".format(tag, page))
        soup = BeautifulSoup(markup = response, features = "html.parser") 
        content = soup.find('div', { 'class':'content'} )
        wpminis = content.find_all('div', { 'class':'wpmini' } )
        ids = []

        for wpmini in wpminis:
            try:
                a = wpmini.find('a')
                img = a.find('img')
                img_id = img.get('src').rsplit('/', 1)[-1]      # split url and get last (id.jpg)
                img_id = os.path.splitext(img_id)[0]            # remove ext (id)
                ids.append(img_id)
            except:
                pass
        return random.choice(ids)

    async def parse_image_url(self, img_id):
        response = await self.get_response_text('https://erowall.com/w/{}/'.format(img_id))
        soup = BeautifulSoup(markup=response, features="html.parser") 
        viewwallpaper = soup.find('div', { 'class':'viewwallpaper'} )

        try:
            a = viewwallpaper.find('a', { 'class':'img' })
            img = a.find('img')
            url = img.get('src')
            return 'https://erowall.com/{}'.format(url)  
        except:
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