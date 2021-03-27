import requests
import json

from discord.ext import commands

from commands.course import CourseCommand
from commands.exchange.account import Account

class ExchangeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name = "биржа", help = "торговля в бирже")
    async def execute(self, context, *args):
        # !биржа [подкоманда] [аргумент]
        if len(args) == 0:
            return await context.send(self.help())

        subcommand_name = self._get_subcommand_name(args[0])
        arg = None if len(args) == 1 else args[1]

        subcommand = getattr(self, subcommand_name, 'help') 
        account = Account(context.message.author, CourseCommand.get_bitcoin_cost())
        message = subcommand(account, arg)
        return await context.send(message)

    def account(self, instance, _=None):
        message = ':moneybag: Ваш счет: {} $'.format(str(instance.get_dollars())) + '\n'
        message += ':coin: BTC: {}'.format(str(instance.get_bitcoins()))
        return message

    def buy(self, account, amount):
        return account.buy(amount)

    def sell(self, account, percent):
        return account.sell(percent)

    def help(self, _=None, __=None):
        return ':exclamation: Команды: \n!биржа аккаунт \n!биржа продать [процент] \n!биржа купить [сумма]'

    def _get_subcommand_name(self, aliase):
        return {
        'купить':'buy',
        'продать':'sell',
        'аккаунт':'account',
        'помощь':'help'
        }.get(aliase, 'help')

def setup(bot):
    bot.add_cog(ExchangeCommand(bot))