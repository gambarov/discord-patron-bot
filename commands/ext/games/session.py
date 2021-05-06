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

        self._handlers = {}
        self._launched = False

    def add_handler(self, event_name: str, func) -> None:
        self._handlers[event_name] = func

    async def update(self, event_name: str, **kwargs):
        if event_name in self._handlers:
            await self._handlers[event_name](**kwargs)

    def close(self) -> None:
        self._launched = False
        self.manager.remove_session(self.message.id)

    def launch(self) -> None:
        self._launched = True

    @property
    def launched(self) -> bool:
        return self._launched and self.players.ready

    @property
    def full(self) -> bool:
        return self.players.full
