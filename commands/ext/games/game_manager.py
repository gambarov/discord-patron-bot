from .game_session import GameSession

class GameManager():
    def __init__(self) -> None:
        self.sessions = {}

        def process(check):
            def wrapper(session):
                if not session.ready():
                    return 'preparing'
                state = check(session)
                return state
            return wrapper

        def add_session(self, message_id, session):
            self.sessions[message_id] = session

        def get_session(self, message_id):
            return self.sessions[message_id]

        def remove_session(self, message_id):
            if self.sessions.get(message_id, None):
                del self.sessions[message_id]

    
