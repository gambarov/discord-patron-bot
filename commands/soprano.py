import random

import discord
from discord.ext import commands

class SopranoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "сопрано", help = "русская рулетка")
    async def execute(self, context):
        # Получаем всех участников канала
        members = context.message.channel.members
        # Удаляем из списка всех ботов
        members = [ member for member in members if not member.bot ]
        # Перемешиваем участников
        random.shuffle(members)
        # Кол-во выстрелов: макс. 6, либо меньше, если меньше участников
        count = min(6, len(members))

        embed = discord.Embed(colour = 0x42F56C)

        for i, member in enumerate(members):
            # Последний выстрел = 100%
            if i == 5:
                embed.add_field(name = member.name, value = 'застрелился', inline=False)
                embed.colour = 0xE02B2B
                break
            # Шанс выстрела
            if self.possibly():
                embed.add_field(name = member.name, value = 'застрелился', inline=False)
                embed.colour = 0xE02B2B
                break
            else:
                embed.add_field(name = member.name, value = 'выжил', inline=False)
        
        await context.send(embed = embed)

    def possibly(self):
        return random.randrange(1, 100) <= 17

def setup(bot):
    bot.add_cog(SopranoCommand(bot))