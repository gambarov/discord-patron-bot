import discord, logging

class UndefinedPlayerTypeException(Exception):
    pass

class PlayerAlreadyExistsException(Exception):
    pass

logger = logging.getLogger('discord')

class GameSession():
    def __init__(self, message_id, grid) -> None:
        self.id = message_id
        self.grid = grid
        self.players = { 'first':None, 'second':None, 'current':None }

    def register(self, player_type: str, user: discord.abc.User):
        # Неизвестный тип игрока
        if not player_type in self.players:
            raise UndefinedPlayerTypeException
        # Если игрок с данным типом уже зарегистрирован
        if isinstance(self.players[player_type], discord.abc.User):
            raise PlayerAlreadyExistsException
        self.players[player_type] = user

    def move_current_player(self, default: discord.abc.User = None):
        current = self.get_player('current')
        first = self.get_player('first')
        second = self.get_player('second')
        # Если текущий игрок существует
        if current:
            # Если текущий игрок был первым, то сейчас второй, иначе наоборот
            current = first if current == second else second
            # Если юзер это не данный текущий игрок
            if current != default:
                return
            self.players['current'] = current
            return current
        # Если второго игрока еще не существует, но при этом существует первый, и полученный пользователь это не первый игрок
        if first and first != default and not second:
            # Добавляем его и возвращаем как текущего
            self.register('second', default)
            # Помечаем как текущего игрока
            self.register('current', default)
            return default
        # Если еще даже первого игрока не существует
        if not first:
            # ВНИМАНИЕ: т.к. второй игрок еще не существует, то текущий игрок (второй) еще не определяется
            self.register('first', default)
            return default

    def get_player(self, player_type):
        # Неизвестный тип игрока
        if not player_type in self.players:
            raise UndefinedPlayerTypeException
        player = self.players[player_type]
        if isinstance(player, discord.abc.User):
            return self.players[player_type]

    def get_player_type(self, user: discord.abc.User):
        return list(self.players.keys())[list(self.players.values()).index(user)]