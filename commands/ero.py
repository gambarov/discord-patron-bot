import requests
import discord
from discord.ext import commands

import io, os
import aiohttp
import requests

import random

from bs4 import BeautifulSoup

class EroCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ero", help = "some ero")
    async def execute(self, context, *, tag='pussy'):

        image_name = self.get_random_image_name(tag)

        if not image_name:
            return await context.send('Can\'t get image name')

        url = self.get_image_url(image_name)

        if not url:
            return await context.send('Can\'t get image')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                if response.status != 200:
                    return await context.send('Could\'nt download file...')
                
                data = io.BytesIO(await response.read())
                await context.send(file=discord.File(data, '{}.png'.format(tag), spoiler=True))

    def get_random_image_name(self, tag):
        page = random.choice(range(1, self.get_max_page(tag)))
        response = requests.get('https://erowall.com/teg/{}/page/{}'.format(tag, page))

        if response.status_code != 200:
            return None
        
        names = []
        soup = BeautifulSoup(markup=response.text, features="html.parser") 
        content = soup.find('div', { 'class':'content'} )
        wpminis = content.find_all('div', { 'class':'wpmini' } )

        for wpmini in wpminis:
            a = wpmini.find('a')
            if a:
                img = a.find('img')
                if img:
                    url = img.get('src')                
                    name = url.rsplit('/', 1)[-1]       # split url and get last (name.jpg)
                    name = os.path.splitext(name)[0]    # remove ext (.jpg)
                    names.append(name)

        return random.choice(names)

    def get_image_url(self, name):
        response = requests.get('https://erowall.com/w/{}/'.format(name))
        
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(markup=response.text, features="html.parser") 
        viewwallpaper = soup.find('div', { 'class':'viewwallpaper'} )

        if viewwallpaper:
            a = viewwallpaper.find('a', { 'class':'img' })
            if a:
                img = a.find('img')
                if img:
                    url = img.get('src')
                    return 'https://erowall.com/' + url 
        return None

    def get_max_page(self, tag):
        response = requests.get('https://erowall.com/search/{}/'.format(tag))

        if response.status_code != 200:
            print('get_max_page: status_code' + str(response.status_code))
            return 2

        soup = BeautifulSoup(markup=response.text, features="html.parser") 
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

def setup(bot):
    bot.add_cog(EroCommand(bot))