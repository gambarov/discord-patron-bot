from .session import GameSession


class GameManager():
    def __init__(self, *states) -> None:
        self.sessions = {}
        self.states = list(['preparing'])
        self.states.extend(states)

        def handler(process):
            def wrapper(session):
                session.state = 'preparing' if not session.ready() else process(session)
                return session.state
            return wrapper

        def add_session(self, message_id, session):
            session.manager = self
            self.sessions[message_id] = session

        def get_session(self, message_id):
            return self.sessions[message_id]

        def remove_session(self, message_id):
            if self.sessions.get(message_id, None):
                del self.sessions[message_id]
