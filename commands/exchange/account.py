from tinydb import TinyDB, Query
db = TinyDB('commands/exchange/db.json')

class Account:
    def __init__(self, member, bitcoin_cost):
        self._bitcoin_cost = bitcoin_cost
        self.member = member
        # Ищем пользователя с его id
        user = next(iter(db.search(Query().id == member.id)), None)
        # Новый пользователь
        if not user:
            db.insert({ 'id':member.id, 'dollars':1000, 'bitcoins':0 })
            user = next(iter(db.search(Query().id == member.id)), None)
        
        self._dollars = user['dollars']
        self._bitcoins = user['bitcoins']

    def get_dollars(self):
        return self._dollars

    def get_bitcoins(self):
        return self._bitcoins

    def buy(self, amount):
        try:
            amount = int(amount)
        except:
            amount = False

        if not amount:
            return ':no_entry_sign: Укажите корректное кол-во $'

        if self._dollars < amount:
            return ':no_entry_sign: Недостаточно средств'

        bitcoins = amount / self._bitcoin_cost
        self._dollars = self._dollars - amount
        self._bitcoins = self._bitcoins + bitcoins 
        db.update({ 'dollars':self._dollars, 'bitcoins':self._bitcoins }, Query().id == self.member.id)
        return ':gear: Вы успешно приобрели {} BTC за {} $'.format(bitcoins, amount)

    def sell(self, percent):
        try:
            percent = int(percent)
        except:
            percent = False

        if not percent:
            return ':no_entry_sign: Укажите корректный % продажи'

        if percent < 1 or percent > 100:
            return ':no_entry_sign: Указан некорректный % продажи'

        bitcoins_to_sell = (self._bitcoins * percent) / 100
        dollars_for_get = bitcoins_to_sell * self._bitcoin_cost
        dollars_for_get = round(dollars_for_get, 2)

        self._dollars += dollars_for_get
        self._bitcoins -= bitcoins_to_sell
        db.update({ 'dollars':self._dollars, 'bitcoins':self._bitcoins }, Query().id == self.member.id)
        return ':gear: Вы успешно продали {} BTC за {} $'.format(bitcoins_to_sell, dollars_for_get)

        


        
