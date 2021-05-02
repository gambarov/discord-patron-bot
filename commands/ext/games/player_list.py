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

    def set_winner(self, winner: GamePlayer) -> None:
        for player in self._players:
            if player == winner:
                return self.winners.append(player)

    def find(self, user: config.UserType) -> GamePlayer:
        for player in self._players:
            if player.user == user:
                return player

    @property
    def deque(self):
        if not self._deque:
            self._deque = deque(self._players)
        return self._deque

    @property
    def current(self):
        if self.deque:
            return self.deque[0]

    def insert(self, index, player: GamePlayer) -> None:
        if self.full() or self.find(player.user):
            return
        self._deque.insert(index, player)
        self._players.insert(index, player)

    def pop(self) -> GamePlayer:
        # no players in self._players
        if not self.deque:
            return None
        return self._deque.popleft()

    def full(self) -> bool:
        return len(self._players) >= self.maxlen

    def ready(self) -> bool:
        l = len(self._players)
        return l >= self.minlen and l % self.step == 0

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

    def __contains__(self, player: GamePlayer):
        for p in self._players:
            if p == player:
                return True

    def __str__(self) -> str:
        return str(self._players)
