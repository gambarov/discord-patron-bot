import discord
import logging
from discord.ext import commands

import io
import os
import aiohttp

import random

from bs4 import BeautifulSoup

from utils.checks import is_vip_user
from utils.helper import get_discord_color, get_error_embed

logger = logging.getLogger(__name__)


class EroCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = {}
        self.client = aiohttp.ClientSession()

    @commands.command(name="ero", help="some ero")
    @commands.check_any(commands.is_owner(), is_vip_user())
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.channel)
    async def execute(self, ctx, *, tag=''):
        async with ctx.typing():
            # Если не указан тег, сразу генерируем рандомный ИД картинки 
            img_id = random.randrange(1, 32000) if not tag else await self.parse_random_image_id(tag)
            img_url = await self.parse_image_url(img_id)
            response = await self.client.get(img_url)
            data = io.BytesIO(await response.read())
            await ctx.send(file=discord.File(data, f'{str(img_id)}.png', spoiler=True))

    @execute.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, AttributeError):
                return await ctx.send(embed=get_error_embed(desc="Такого раздела не существует"))
        if isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(embed=discord.Embed(title="⛔ Доступ ограничен", description="Команда доступна только для VIP-пользователей", colour=get_discord_color('error')))
        logger.exception(error)
        await ctx.send(embed=get_error_embed(desc="Не удалось получить фото"))

    async def parse_random_image_id(self, tag):
        page = random.choice(range(1, await self.parse_max_page(tag) + 1))
        response = await self.client.get(f"https://erowall.com/teg/{tag}/page/{page}")
        soup = BeautifulSoup(markup=await response.text(), features="html.parser")
        content = soup.find('div', {'class': 'content'})
        wpminis = content.find_all('div', {'class': 'wpmini'})
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
        response = await self.client.get(f"https://erowall.com/w/{str(img_id)}/")
        soup = BeautifulSoup(markup=await response.text(), features="html.parser")
        viewwallpaper = soup.find('div', {'class': 'viewwallpaper'})

        try:
            a = viewwallpaper.find('a', {'class': 'img'})
            img = a.find('img')
            url = img.get('src')
            return 'https://erowall.com/{}'.format(url)
        except:
            return None

    async def parse_max_page(self, tag):
        try:
            return self.tags[tag]['max_page']
        except:
            pass

        response = await self.client.get(f"https://erowall.com/search/{tag}/")
        soup = BeautifulSoup(
            markup=await response.text(),
            features="html.parser")
        paginator = soup.find('div', {'class': 'paginator'})
        ul = paginator.find('ul')
        num = 1
        for li in ul.find_all('li'):
            try:
                num = int(li.find('a').string)
            except:
                pass
        # Кешируем данные
        self.tags[tag] = {'max_page': num}
        return num


def setup(bot):
    bot.add_cog(EroCommand(bot))
