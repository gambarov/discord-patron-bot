import random

from discord.ext import commands

class WhoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "кто", help = "выбор случайного участника")
    async def execute(self, context, *phrase):
        # Получаем всех участников канала
        members = context.message.channel.members
        # Удаляем из списка всех ботов
        members = [ member for member in members if not member.bot ]
        member = random.choice(members)
        texts = [ "Бля буду,", "По-любому", "Очевидно, что", "Скорее всего," ]
        # Объединяем список элементов кортежа в одну строку (если он существует)
        phrase = ' '.join(map(str, phrase)) 
        await context.send('{} {} {}'.format(random.choice(texts), member.name, phrase))

def setup(bot):
    bot.add_cog(WhoCommand(bot))