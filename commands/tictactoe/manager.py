import logging
from commands.tictactoe.session import GameSession

logger = logging.getLogger('discord')


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

    def check_for_winner(self, session: GameSession):
        for player in session.players():
            def check_matrix(matrix):
                # По горизонтали
                for x in range(len(matrix)):
                    for y in range(len(matrix[x])):
                        if matrix[x][y]['emoji'] != player.emoji:
                            break
                        elif y == len(matrix) - 1:
                            return True
                # По вертикали
                for x in range(len(matrix)):
                    for y in range(len(matrix[x])):
                        if matrix[y][x]['emoji'] != player.emoji:
                            break
                        elif y == len(matrix) - 1:
                            return True
                # По главной диагонали
                for i in range(len(matrix)):
                    if matrix[i][i]['emoji'] != player.emoji:
                        break
                    elif i == len(matrix) - 1:
                        return True
                # По обратной диагонали
                for x in range(len(matrix)):
                    y = len(matrix)-1-x
                    if matrix[x][y]['emoji'] != player.emoji:
                        break
                    elif x == len(matrix) - 1:
                        return True

            matrix = session.grid.matrix
            if check_matrix(matrix):
                return player
