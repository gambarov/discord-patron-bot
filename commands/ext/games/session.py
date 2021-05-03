import logging
from .player_list import GamePlayerList

logger = logging.getLogger(__name__)


class GameSession():
    def __init__(self, manager, message, min_players: int, max_players: int, step_players: int, **options) -> None:
        self.manager = manager
        self.players = GamePlayerList(min_players, max_players, step_players)
        self.message = message
        
        for key, value in options.items():
            assert(getattr(self, key, None) is None)
            setattr(self, key, value)

        self._manager = None
        self._launched = False
        self._state = None

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
        else:
            logger.info(f"Session #{self.message.id}: new state is '{new_state}'")
            self._state = new_state

    def launch(self):
        self._launched = True

    @property
    def launched(self):
        return self._launched and self.players.ready()

    def full(self):
        return self.players.full()
