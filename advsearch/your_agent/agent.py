import random
import math
import copy
from ..othello import board

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada com as pretas.
    # Remova-o e coloque a sua implementacao da poda alpha-beta
    othello_state = OthelloState(the_board, color)
    return othello_state.random_move()


class OthelloState:
    def __init__(self, the_board: board, agent_color: str):
        self.the_board = the_board
        self.agent_color = agent_color
        self.rival_color = "W" if agent_color == "B" else "B"

    def valid_moves(self):
        valid_moves = self.the_board.legal_moves(self.agent_color)
        return valid_moves

    def random_move(self):
        if len(self.valid_moves()) > 0:
            return random.choice(self.valid_moves())
        else:
            return (-1, -1)
