import logging
from .player_list import GamePlayerList
from .manager import GameManager

logger = logging.getLogger(__name__)


class GameSession():
    def __init__(self, message_id: int, min_players: int, max_players: int, step_players: int, **options) -> None:
        self.players = GamePlayerList(min_players, max_players, step_players)
        self.message_id = message_id
        self.options = options
        self._manager = None
        self._ready = False
        self._state = 'preparing'

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, manager: GameManager):
        self._manager = manager

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: str):
        assert(self.manager)
        assert(new_state in self.manager.states)
        logger.info(f"Session #{self.message_id}: new state is '{new_state}'")
        self._state = new_state

    def launch(self):
        self._ready = True

    def ready(self):
        return self._ready and self.players.ready()

    def full(self):
        return self.players.full()
