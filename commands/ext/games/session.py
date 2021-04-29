import logging
from .player_list import GamePlayerList

logger = logging.getLogger(__name__)


class GameSession():
    def __init__(self, manager, message, min_players: int, max_players: int, step_players: int, **options) -> None:
        self.manager = manager
        self.players = GamePlayerList(min_players, max_players, step_players)
        self.message = message
        self.options = options
        self._manager = None
        self._ready = False
        self._state = 'preparing'

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: str):
        assert(self.manager)
        try:
            assert(new_state in self.manager.states)
        except:
            logger.error(f"Incorrect state: {new_state} (available states: {str(self.manager.states)})")
        logger.info(f"Session #{self.message.id}: new state is '{new_state}'")
        self._state = new_state

    def launch(self):
        self._ready = True

    def ready(self):
        return self._ready and self.players.ready()

    def full(self):
        return self.players.full()
