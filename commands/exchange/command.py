from discord.ext import commands

from commands.course import CourseCommand
from commands.exchange.account import Account

class ExchangeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name = "биржа", help = "торговля в бирже")
    async def execute(self, ctx, subcommand, *, arg=None):
        # Получаем название подкоманды
        subcommand_name = self._get_subcommand_name(subcommand)
        # Пытаемся получить подкоманду
        command = getattr(self, subcommand_name, 'help') 
        account = Account(ctx.message.author, CourseCommand.get_bitcoin_cost())
        # Вызов подкоманды
        message = command(account, arg)
        return await ctx.send(message)

    @execute.error
    async def info_error(self, ctx, error):
        return await ctx.send(self.help())

    def account(self, instance, _=None):
        message = ':moneybag: Ваш счет: {} $'.format(str(instance.dollars)) + '\n'
        message += ':coin: BTC: {}'.format(str(instance.bitcoins))
        return message

    def buy(self, account, amount):
        return account.buy(amount)

    def sell(self, account, percent):
        return account.sell(percent)

    def help(self, _=None, __=None):
        return ':exclamation: Команды: \n!биржа аккаунт \n!биржа продать [%] \n!биржа купить [$]'

    def _get_subcommand_name(self, aliase):
        return {
        'купить':'buy',
        'продать':'sell',
        'аккаунт':'account',
        'помощь':'help'
        }.get(aliase, 'help')

def setup(bot):
    bot.add_cog(ExchangeCommand(bot))