import logging
from .player_list import GamePlayerList

logger = logging.getLogger(__name__)


class GameSession():
    def __init__(self, message_id: int, min_players: int, max_players: int, step_players: int, **options) -> None:
        self.players = GamePlayerList(min_players, max_players, step_players)
        self.message_id = message_id
        self.options = options
        self._ready = False

    def launch(self):
        self._ready = True

    def ready(self):
        return self._ready and self.players.ready()

    def full(self):
        return self.players.full()
