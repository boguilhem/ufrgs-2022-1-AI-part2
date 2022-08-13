import random
import math
from copy import deepcopy
from typing import Tuple
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
    return othello_state.minimax_strategy(color, the_board)


class OthelloState:
    def __init__(self, board: board, agent_color: str):
        self.board = board
        self.agent_color = agent_color
        self.rival_color = "W" if agent_color == "B" else "B"
        self.num_player_moves = 0
        self.num_opponent_moves = 0

    def minimax_strategy(self, color, board) -> Tuple[int, int]:
        valid_moves = board.legal_moves(color)

        if len(valid_moves) == 0:
            return (-1, -1)

        agent_movement = random.choice(valid_moves)

        alpha = -math.inf
        beta = math.inf

        for move in valid_moves:
            evaluation = self.minimax_alpha_beta(board, 3, alpha, beta, color)

            if evaluation > alpha:
                alpha = evaluation
                agent_movement = move
        return agent_movement

    def minimax_alpha_beta(self, board: board, depth: int, alpha, beta, color: str):
        valid_moves = board.legal_moves(color)
        num_valid_moves = len(valid_moves)

        if depth == 0 or board.is_terminal_state():
            return self.heuristics_eval(board, color)

        if color == self.agent_color:
            self.num_player_moves = num_valid_moves
            max_eval = -math.inf
            for move in valid_moves:
                virtual_board = deepcopy(board)
                virtual_board.process_move(move, color)
                evaluation = self.minimax_alpha_beta(virtual_board, depth - 1, alpha, beta, self.rival_color)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval

        else:
            self.num_opponent_moves = num_valid_moves
            min_eval = math.inf
            for move in valid_moves:
                virtual_board = deepcopy(board)
                virtual_board.process_move(move, color)
                evaluation = self.minimax_alpha_beta(virtual_board, depth - 1, alpha, beta, self.agent_color)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def piece_score(self, board: board, color: str):
        agent_pieces = board.num_pieces(color)
        rival_pieces = board.num_pieces(self.rival_color)

        score = agent_pieces - rival_pieces
        return score

    def movements_score(self):
        """
        Retorna o numero de jogadas possiveis do oponente
        :return: int
        """
        # numero de jogadas possiveis do jogador
        player_moves = self.num_player_moves

        # # numero de jogadas possiveis do oponente
        opponent_moves = self.num_opponent_moves

        # retorna o score baseado na quantidade de movimentos possíveis
        if opponent_moves + player_moves != 0:
            movement_score = 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
        else:
            movement_score = 0

        return movement_score

    WEIGHT_MAP = [
        [100, -10, 20, 10, 10, 20, -10, 100],
        [-10, -20, 1, 1, 1, 1, -20, -10],
        [15, 1, 10, 5, 5, 10, 1, 15],
        [10, 1, 5, 5, 5, 5, 1, 10],
        [10, 1, 5, 5, 5, 5, 1, 10],
        [15, 1, 10, 5, 5, 10, 1, 15],
        [-10, -20, 1, 1, 1, 1, -20, -10],
        [100, -10, 20, 10, 10, 20, -10, 100],
    ]

    def map_score(self):
        agent_score = 0
        rival_score = 0

        for x in range(8):
            for y in range(8):
                if self.board.tiles[x][y] == self.agent_color:
                    agent_score += self.WEIGHT_MAP[x][y]
                elif self.board.tiles[x][y] == self.rival_color:
                    rival_score += self.WEIGHT_MAP[x][y]
        return agent_score - rival_score

    def heuristics_eval(self):
        movements_score_heuristic = self.movements_score() * 0.3
        map_score_heuristic = self.map_score() * 0.7
        final_heuristic = map_score_heuristic + movements_score_heuristic
        return final_heuristic
