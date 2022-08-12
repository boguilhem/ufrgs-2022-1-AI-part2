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
    # print("RETORNO DO MAKE MOVE: ", othello_state.minimax_strategy(color, the_board))
    return othello_state.minimax_strategy(color, the_board)
    # return othello_state.random_move(color)


class OthelloState:
    def __init__(self, board: board, agent_color: str):
        self.board = board
        self.agent_color = agent_color
        self.rival_color = "W" if agent_color == "B" else "B"

    def random_move(self, color: str):
        virtual_board = deepcopy(self.board)
        valid_moves = virtual_board.legal_moves(color)
        if len(valid_moves) > 0:
            return random.choice(valid_moves)
        else:
            return (-1, -1)

    def minimax_strategy(self, color, board) -> Tuple[int, int]:
        valid_moves = board.legal_moves(color)

        if len(valid_moves) == 0:
            # print("LEN DE MOVES É ZERO")
            return (-1, -1)

        agent_movement = random.choice(valid_moves)
        # print("AGENT_MOVEMENT: ", agent_movement)

        alpha = -math.inf
        beta = math.inf

        for move in valid_moves:
            # virtual_board = deepcopy(board)
            # virtual_board.process_move(move, self.agent_color)
            # evaluation = self._min_score(test_board, self.opponent_color, -INFINITY, INFINITY, self.depth_limit - 1)
            evaluation = self.minimax_alpha_beta(board, 2, alpha, beta, color)

            if evaluation > alpha:
                alpha = evaluation
                agent_movement = move
        # print("MOVIMENTO FINAL: ", agent_movement)
        print("ALPHA: ", alpha)
        return agent_movement

    def minimax_alpha_beta(self, board: board, depth: int, alpha, beta, color: str):
        valid_moves = board.legal_moves(color)
        # print("MOVIMENTOS VALIDOS: ", valid_moves)

        if depth == 0 or board.is_terminal_state():
            # print("DEPTH É ZERO")
            return self.heuristics_eval(board, color)

        if color == self.agent_color:
            # print("ENTROU NO MAX")
            max_eval = -math.inf
            for move in valid_moves:
                virtual_board = deepcopy(board)
                virtual_board.process_move(move, color)
                evaluation = self.minimax_alpha_beta(virtual_board, depth - 1, alpha, beta, self.rival_color)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            # print("MAX_EVAL: ", max_eval)
            return max_eval

        else:
            # print("ENTROU NO MIN")
            min_eval = math.inf
            for move in valid_moves:
                virtual_board = deepcopy(board)
                virtual_board.process_move(move, color)
                evaluation = self.minimax_alpha_beta(virtual_board, depth - 1, alpha, beta, self.agent_color)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            # print("MIN_EVAL: ", min_eval)
            return min_eval

    def heuristics_eval(self, board, color):
        piece_score_heuristic = self.piece_score(board, color)
        final_heuristic = piece_score_heuristic
        # print("HEURISTICS EVAL: ", final_heuristic)
        return final_heuristic

    def piece_score(self, board: board, color: str):
        rival_pieces = board.num_pieces(self.rival_color)
        agent_pieces = board.num_pieces(color)

        score = agent_pieces - rival_pieces
        return score
