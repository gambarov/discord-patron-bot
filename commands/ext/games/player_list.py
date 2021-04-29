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
                logger.info(f"Appending player '{player.user.name}' to winners")
                return self.winners.append(player)

    def find(self, user: config.UserType) -> GamePlayer:
        for player in self._players:
            if player.user == user:
                return player

    @property
    def _current_deque(self):
        if not self._deque:
            self._deque = deque(self._players)
        return self._deque

    @property
    def current(self):
        if self._current_deque:
            player = self._current_deque[0]
            logger.info(f"Current player is '{player.user.name}'")
            return player
        logger.info(f"Current player is None")

    def insert(self, index, player: GamePlayer) -> None:
        if self.full():
            logger.warn("Can't add user to session: limit is exceeded!")
            return
        if self.find(player.user):
            logger.warn(f"Player '{player.user.name}'' already exists!")
            return
        logger.info(f"Inserting player '{player.user.name}'")
        self._deque.insert(index, player)
        self._players.insert(index, player)

    def full(self) -> bool:
        return len(self._players) >= self.maxlen

    def ready(self) -> bool:
        l = len(self._players)
        return l >= self.minlen and l % self.step == 0

    def pop(self) -> GamePlayer:
        if not self._current_deque:
            logger.info("Can't pop: deque of players is empty because there are no players")
            return None
        player = self._current_deque.popleft()
        logger.info(f"Popping player '{player.user.name}'")
        return player

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
