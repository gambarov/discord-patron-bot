import collections
import logging

from . import config
from .player import GamePlayer

logger = logging.getLogger(__name__)


class GamePlayerList(collections.MutableSequence):
    def __init__(self, minlen: int, maxlen: int, step: int = 1) -> None:
        self._players = list()
        self.winners = list()
        self.minlen = minlen
        self.maxlen = maxlen
        self.step = step

    def set_winner(self, user: config.UserType) -> None:
        for player in self._players:
            if player.user == user:
                return self.winners.append(player)

    def find(self, user: config.UserType) -> GamePlayer:
        for player in self._players:
            if player.user == user:
                return player

    def insert(self, index, player: GamePlayer) -> None:
        if self.full():
            logger.warn("Can't add user to session: limit is exceeded!")
            return
        if self.find(player.user):
            logger.warn("Player already exists!")
            return
        self._players.insert(index, player)

    def full(self) -> bool:
        return len(self._players) >= self.maxlen

    def ready(self) -> bool:
        l = len(self._players)
        return l >= self.minlen and l % self._step == 0

    def move_next(self, user: config.UserType):
        # Сессия еще не готова, просто добавляем и возвращаем игроков по очереди
        if not self.full:
            # Пользователь уже зарегистрирован
            if self.find(user):
                return None
            player = self.add(user)
            self.previous = player
            return player
        # Если пытается походить пред игрок
        if self.previous:
            if self.previous.user == user:
                return False
        # Пытаемся получить игрока
        player = self.get(user)
        # Иначе в зависимости от пред игрока определяем текущего (если юзер - это существующий игрок)
        if player:
            current = next(itertools.cycle(self.players))
            self.previous = current
            return current

    def __len__(self):
        return len(self._players)

    def __getitem__(self, key):
        return self._players[key]

    def __setitem__(self, key, value):
        self._players[key] = value

    def __delitem__(self, key):
        del self._players[key]

    def __iter__(self):
        yield from self._players

    def __contains__(self, user: config.UserType):
        for player in self._players:
            if player.user == user:
                return True

    def __str__(self) -> str:
        return str(self._players)
