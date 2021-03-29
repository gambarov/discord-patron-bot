import random

from discord.ext import commands
import datetime

class WhenCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "когда", help = "через сколько наступит та или иная дата")
    async def execute(self, context, *, phrase = ''):
        generators = [ 'generate1', 'generate2', 'generate3' ]
        generator = random.choice(generators)
        message = getattr(self, generator)(phrase)
        await context.send(message)

    def generate1(self, phrase = ''):
        texts = [ 'Это случится', 'Это произойдет' ]
        now = datetime.datetime.now()
        start_date = datetime.date(int(now.year), int(now.month), int(now.day))
        end_date = datetime.date(2065, 1, 1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        date = start_date + datetime.timedelta(days=random_number_of_days)
        return '{} {}'.format(phrase or random.choice(texts), date)

    def generate2(self, phrase = ''):
        texts = [ 'Завтра', 'На следующей неделе', 'Через месяц', 'Через год', 'Никогда' ]
        return '{} {}'.format(random.choice(texts), phrase)

    def generate3(self, phrase = ''):
        times = [ 'часов', 'дней', 'месяцев', 'лет' ]
        return 'Через {} {} {}'.format(random.choice(range(1, 21)), random.choice(times), phrase)

def setup(bot):
    bot.add_cog(WhenCommand(bot))