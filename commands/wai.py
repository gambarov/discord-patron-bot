import random
import time

from discord.ext import commands

class WaiCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wai_strs = [
            'Аѓузу биллаћи минєш-шєйтанир-ражим',
            'Бисмиллаћир рахманир рахим!',
            'Єл-хємду лил-ллєєћи робил ъааламиин.',
            'Ар-рохмєєнир-рохиим. Мєєлики яумид-диин.',
            'Ийєєкє наъбуду уа ийакє настаъиин.',
            'Сыйроотал-лєзиина єнъамтє ъалейћим.',
            'Ѓойрил-Маѓдууби ъалейћим ує лєд-дооллиин!',
            'Агузу биллахи минаш-шайтанир-ражим',
            'Бисмиллахир рахманир рахим!',
            'Аль-хамду лил-лляяхи робил ъааламиин.',
            'Ар-рохмаанир-рохиим. Маалики яумид-диин.',
            'Ийаака наъбуду уа ийака настаъиин.',
            'Сыйроотал-лазиина анъамта ъалейхим.',
            'Гойрил-Магдууби галейхим уа лад-дооллиин!'
        ]

    @commands.command(name = "вайдавай", help = "вааай!")
    async def execute(self, context):
        while True:
            for wai in self.wai_strs:
                time.sleep(10)
                await context.send(wai)

def setup(bot):
    bot.add_cog(WaiCommand(bot))