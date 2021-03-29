from tinydb import TinyDB, Query
db = TinyDB('commands/exchange/db.json')

import discord
from commands.course import CourseCommand

class EconomyException(Exception):
    def __init__(self, message, colour):
        self.message = message
        self.colour = colour
        super().__init__(message)

class Economy():
    @staticmethod 
    async def buy(member, amount = 100):
        try:
            amount = int(amount)
            if amount < 1: raise Exception()            
        except:
            raise EconomyException(":no_entry_sign: Укажите корректное кол-во $", 0xE02B2B)

        account = Economy.get(member)

        if account['dollars'] < amount:
            raise EconomyException(":no_entry_sign: Недостаточно средств", 0xE02B2B)

        bitcoins_to_get = amount / await CourseCommand.get_bitcoin_cost()
        Economy.update(member, account['dollars'] - amount, account['bitcoins'] + bitcoins_to_get)
        return bitcoins_to_get

    @staticmethod
    async def sell(member, percent = 100):
        try:
            percent = int(percent)
            if percent < 1 or percent > 100: raise Exception()
        except:
            raise EconomyException(":no_entry_sign: Укажите корректный % продажи", 0xE02B2B)

        account = Economy.get(member)

        if account['bitcoins'] == 0:
            raise EconomyException(":warning: На счету отсутствуют BTC", 0xF59E42)

        bitcoins_to_sell = (account['bitcoins'] * percent) / 100
        dollars_to_get = bitcoins_to_sell * (await CourseCommand.get_bitcoin_cost())
        dollars_to_get = round(dollars_to_get, 2)
        
        Economy.update(member, account['dollars'] + dollars_to_get, account['bitcoins'] - bitcoins_to_sell)
        return bitcoins_to_sell

    @staticmethod
    def update(member, dollars, bitcoins):
        dollars = abs(round(dollars, 2))
        bitcoins = abs(bitcoins)
        db.update({ 'dollars':dollars, 'bitcoins':bitcoins }, Query().id == member.id)

    @staticmethod
    def get(member):
        assert(isinstance(member, discord.Member) or isinstance(member, discord.User))
        user = next(iter(db.search(Query().id == member.id)), None)
        # Новый пользователь
        if not user:
            user = { 'id':member.id, 'dollars':1000, 'bitcoins':0 }
            db.insert(user)
        return user