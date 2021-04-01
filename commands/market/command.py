import discord, logging

from discord.ext import commands
from commands.market.economy import Economy, EconomyException
from utils.helper import get_discord_color

logger = logging.getLogger('discord')

class ExchangeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(name = "биржа", help = "торговля на бирже")
    async def execute(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.help(ctx)

    @execute.command(name = "аккаунт")
    async def account(self, ctx):
        instance = Economy.get(ctx.author)
        message = ':moneybag: Ваш счет: {} $'.format(str(instance['dollars'])) + '\n'
        message += ':coin: BTC: {}'.format(str(instance['bitcoins']))
        await ctx.send(embed = discord.Embed(description = message, colour = 0x4299F5))

    @execute.command(name = "купить")
    async def buy(self, ctx, amount):
        try:
            bitcoins = await Economy.buy(ctx.author, amount)
            await ctx.send(embed = discord.Embed(description = "Вы успешно приобрели {} BTC за {} $".format(bitcoins, amount), colour = get_discord_color('success')))
        except EconomyException as e:
            await ctx.send(embed = discord.Embed(description = e.message, colour = e.colour))

    @execute.command(name = "продать")
    async def sell(self, ctx, percent):
        try:
            bitcoins = await Economy.sell(ctx.author, percent)
            await ctx.send(embed = discord.Embed(description = "Вы успешно продали {} BTC".format(bitcoins), colour = get_discord_color('success')))
        except EconomyException as e:
            await ctx.send(embed = discord.Embed(description = e.message, colour = e.colour))
    
    @execute.command(name = "помощь")
    async def help(self, ctx):
        message = ":exclamation: Команды: \n!биржа аккаунт \n!биржа продать [%] \n!биржа купить [$]"
        await ctx.send(embed = discord.Embed(description = message, colour = get_discord_color('info')))

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed = discord.Embed(description = ":warning: Укажите аргумент", colour = get_discord_color('warning')))
        logger.exception(error)
        await ctx.send(embed = discord.Embed(description = "Неизвестная ошибка", colour = get_discord_color('error')))

def setup(bot):
    bot.add_cog(ExchangeCommand(bot))