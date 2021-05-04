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
        self.minlen = minlen
        self.maxlen = maxlen
        self.step = step
        self.lost = False

    def set_winner(self, winner: GamePlayer) -> None:
        player = self.find(winner.user)
        if player and not player.ignored:
            player.winner = True

    def ignore(self, player: GamePlayer) -> None:
        player = self.find(player.user)
        if player:
            player.ignored = True
        for player in self._players:
            if not player.ignored:
                return
        self.lost = True

    def find(self, user: config.UserType) -> GamePlayer:
        for player in self._players:
            if player.user == user:
                return player

    @property
    def winners(self) -> list:
        if self.lost:
            return list()
        return [player for player in self._players if player.winner]

    @property
    def deque(self) -> deque:
        if self.lost:
            return None
        if not self._deque:
            self._deque = deque(self._players)
        return self._deque

    @property
    def current(self) -> GamePlayer:
        if self.deque:
            for player in self._deque:
                if not player.ignored:
                    return player

    def insert(self, index, player: GamePlayer) -> None:
        if self.full() or self.find(player.user):
            return
        self._deque.insert(index, player)
        self._players.insert(index, player)

    def pop(self) -> GamePlayer:
        # no players in self._players or all players got ignored
        if not self.deque:
            return None
        player = self._deque.popleft()
        if player.ignored:
            return self.pop()
        return player

    def full(self) -> bool:
        return len(self._players) >= self.maxlen

    def ready(self) -> bool:
        l = len(self._players)
        return l >= self.minlen and l % self.step == 0

    def __len__(self) -> int:
        return len(self._players)

    def __getitem__(self, key) -> GamePlayer:
        return self._players[key]

    def __setitem__(self, key, value) -> None:
        self._players[key] = value

    def __delitem__(self, key) -> None:
        del self._players[key]

    def __iter__(self):
        yield from self._players

    def __contains__(self, x: object) -> bool:
        for player in self._players:
            if player == x:
                return True

    def __str__(self) -> str:
        return str(self._players)
