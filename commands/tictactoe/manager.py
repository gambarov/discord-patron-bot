import logging
from commands.tictactoe.session import Session

logger = logging.getLogger('discord')

emoji_moves = { 'first':'❌', 'second':'⭕' }

class GameManager:
    def __init__(self) -> None:
        self.sessions = {}

    def add_session(self, id, grid):
        self.sessions[id] = Session(id = id, grid = grid)

    def delete_session(self, id):
        del self.sessions[id]

    def get_player_emoji_move(self, player_type):
        return emoji_moves.get(player_type)

    def check_for_draw(self, session):
        return (session.grid.move_count == pow(session.grid.size, 2))

    def check_for_winner(self, session):
        for player_type, player_emoji in emoji_moves.items():
            matrix = session.grid.matrix
            # По горизонтали
            for x in range(len(matrix)):
                for y in range(len(matrix[x])):
                    if matrix[x][y]['emoji'] != player_emoji:
                        break
                    elif y == len(matrix) - 1:
                        del self.sessions[session.id]
                        return session.get_player(player_type)
            # По вертикали
            for x in range(len(matrix)):
                for y in range(len(matrix[x])):
                    if matrix[y][x]['emoji'] != player_emoji:
                        break
                    elif y == len(matrix) - 1:
                        del self.sessions[session.id]
                        return session.get_player(player_type)
            # По главной диагонали
            for i in range(len(matrix)):
                if matrix[i][i]['emoji'] != player_emoji:
                    break
                elif i == len(matrix) - 1:
                    del self.sessions[session.id]
                    return session.get_player(player_type)
            # По обратной диагонали
            for x in range(len(matrix)):
                y = len(matrix)-1-x
                if matrix[x][y]['emoji'] != player_emoji:
                    break
                elif x == len(matrix) - 1:
                    del self.sessions[session.id]
                    return session.get_player(player_type)