import collections
from collections import deque
import logging

from . import config
from .player import GamePlayer

logger = logging.getLogger(__name__)


class GamePlayerList(collections.MutableSequence):
    def __init__(self, minlen: int, maxlen: int, step: int = 1) -> None:
        self._players = list()
        self._deque = deque()
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

    def pop(self):
        if len(self._deque) == 0:
            logger.info("Deque of players is empty, recreating...")
            self._deque = deque(self._players)
        player = self._deque.popleft()
        logger.info(f"Popping player '{player.user.name}'")
        return

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
