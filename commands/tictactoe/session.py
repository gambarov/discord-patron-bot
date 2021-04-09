import discord


class UndefinedPlayerTypeException(Exception):
    pass


class PlayerAlreadyExistsException(Exception):
    pass


class Player():
    def __init__(self, user, typ, emoji) -> None:
        self.user = user
        self.typ = typ
        self.emoji = emoji


class GameSession():
    def __init__(self, message_id, grid) -> None:
        self.id = message_id
        self.grid = grid
        self.first = None
        self.second = None
        self.previous = None

    def players(self):
        players = [ self.second, self.first ]
        return filter(None, players)

    def get(self, user: discord.Member):
        self.add(user)
        if user == self.first.user:
            return self.first
        elif user == self.second.user:
            return self.second
        return False

    def add(self, user: discord.Member):
        if not self.first:
            self.first = Player(user, 'first', '❌')
        elif not self.second and user != self.first.user:
            self.second = Player(user, 'second', '⭕')

    def ready(self):
        return self.first and self.second

    def exists(self, user: discord.Member):
        return self.first.user == user or self.second.user == user

    def move_next(self, user: discord.Member):
        # Пытаемся добавить игрока
        player = self.get(user)
        # Сессия еще не готова, просто добавляем и возвращаем игроков по очереди
        if not self.ready():
            self.previous = player
            return player
        # Иначе в зависимости от пред игрока определяем текущего (если юзер - это существующий игрок)
        elif self.exists(user):
            # Если пытается походить пред игрок
            if self.previous.user == user:
                return False
            current = self.first if self.previous == self.second else self.second
            self.previous = current
            return current
