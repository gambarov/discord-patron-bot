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
        
        self.dollars = user['dollars']
        self.bitcoins = user['bitcoins']

    def buy(self, amount):
        try:
            amount = int(amount)
        except:
            amount = False

        if not amount:
            return ':warning: Укажите корректное кол-во $', 0xF59E42

        if self.dollars < amount:
            return ':no_entry_sign: Недостаточно средств', 0xE02B2B 

        bitcoins_to_get = amount / self._bitcoin_cost
        self._update(self.dollars - amount, self.bitcoins + bitcoins_to_get)
        return ':gear: Вы успешно приобрели {} BTC за {} $'.format(bitcoins_to_get, amount), 0x42F56C

    def sell(self, percent):
        try:
            percent = int(percent)
        except:
            percent = False

        if not percent:
            return ':warning: Укажите корректный % продажи', 0xF59E42

        if percent < 1 or percent > 100:
            return ':no_entry_sign: Указан некорректный % продажи', 0xE02B2B

        bitcoins_to_sell = (self.bitcoins * percent) / 100
        dollars_to_get = bitcoins_to_sell * self._bitcoin_cost

        self._update(self.dollars + dollars_to_get, self.bitcoins - bitcoins_to_sell)
        return ':gear: Вы успешно продали {} BTC за {} $'.format(bitcoins_to_sell, round(dollars_to_get, 2)), 0x42F56C

    def _update(self, dollars, bitcoins):
        self.dollars = round(dollars, 2)
        self.bitcoins = bitcoins
        db.update({ 'dollars':self.dollars, 'bitcoins':self.bitcoins }, Query().id == self.member.id)