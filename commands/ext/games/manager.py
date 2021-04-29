import logging
from .session import GameSession

logger = logging.getLogger(__name__)

class GameManager():
    def __init__(self, *states) -> None:
        self.sessions = {}
        self.states = list(['preparing'])
        self.states.extend(*states)

    def add_session(self, message, max_players, min_players, step_players, **options) -> GameSession:
        session = GameSession(self, message, min_players, max_players, step_players, **options)
        self.sessions[message.id] = session
        return session

    def get_session(self, message_id) -> GameSession:
        return self.sessions.get(message_id, None)

    def remove_session(self, message_id) -> None:
        if self.sessions.get(message_id, None):
            del self.sessions[message_id]

def handler(process):
    async def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        session.state = 'preparing' if not session.ready() else await process(*args, **kwargs)
        return session.state
    return wrapper
