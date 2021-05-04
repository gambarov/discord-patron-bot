import logging

from .session import GameSession

logger = logging.getLogger(__name__)

class GameManager():
    def __init__(self, **kwargs) -> None:
        self.sessions = {}
        self.states = list(kwargs.get('states'))

    def add_session(self, session) -> GameSession:
        self.sessions[session.message.id] = session
        return session

    def get_session(self, message_id) -> GameSession:
        return self.sessions.get(message_id, None)

    def remove_session(self, message_id) -> None:
        if self.sessions.get(message_id, None):
            logger.info(f"Removing session #{message_id}")
            del self.sessions[message_id]

def handler(process):
    async def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        session.state = await process(*args, **kwargs)
        return session.state
    return wrapper
