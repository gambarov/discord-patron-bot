import discord, logging, random
from utils.helper import get_discord_color, get_error_embed
from discord.ext import commands

logger = logging.getLogger('discord')

class LoveMatchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "совм", help = "любовная совместимость")
    async def execute(self, context, *, names):
        names = [ name.strip() for name in names.split(' и ') ]
        if len(names) <= 1:
            return await context.send(embed = get_error_embed(desc = "??"))
        name1 = self.format_name(names[0])
        name2 = self.format_name(names[1])
        percent = random.randrange(1, 101)
        embed = discord.Embed(title = "👥 {} и {}".format(name1, name2), description = "✨ Совместимость: {}% {}".format(str(percent), self.get_emoji(percent)), colour = get_discord_color('info'))
        await context.send(embed = embed)

    def format_name(self, name):
        if name.lower() == "я":
            return 'Ты'
        return name.title()

    def get_emoji(self, percent):
        if percent < 40:
            return '💔'
        elif percent >= 40 and percent < 70:
            return '❤️'
        else:
            return '💖'

    @execute.error
    async def on_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await context.send("Введите имена через 'и'")
        logger.exception(error)
        await context.send(embed = get_error_embed(desc = "Не удалось получить данные"))

def setup(bot):
    bot.add_cog(LoveMatchCommand(bot))