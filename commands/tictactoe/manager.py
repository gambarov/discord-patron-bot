import logging
from commands.tictactoe.session import GameSession


class GameManager:
    def __init__(self) -> None:
        self.sessions = {}

    def add_session(self, message_id, grid):
        self.sessions[message_id] = GameSession(
            message_id=message_id, grid=grid)

    def delete_session(self, message_id):
        del self.sessions[message_id]

    def check_for_draw(self, session: GameSession):
        return (session.grid.move_count == pow(session.grid.size, 2))

    