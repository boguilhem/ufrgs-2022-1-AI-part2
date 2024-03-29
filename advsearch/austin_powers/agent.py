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

        agent_movement = valid_moves[0]

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
            return self.heuristics_eval()

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
        agent_pieces = self.num_player_moves

        # numero de jogadas possiveis do oponente
        rival_pieces = self.num_opponent_moves

        # retorna o score baseado na quantidade de movimentos possíveis
        movement_score = 0
        if rival_pieces + agent_pieces == 0:
            return movement_score
        else:
            movement_score = 100 * (agent_pieces - rival_pieces) / (agent_pieces + rival_pieces)
        return movement_score

    WEIGHT_MAP = [
        [100, -10, 20, 10, 10, 20, -10, 100],
        [-10, -20, -5, -5, -5, -5, -20, -10],
        [15, -5, 10, 5, 5, 10, -5, 15],
        [10, -5, 5, 5, 5, 5, -5, 10],
        [10, -5, 5, 5, 5, 5, -5, 10],
        [15, -5, 10, 5, 5, 10, -5, 15],
        [-10, -20, -5, -5, -5, -5, -20, -10],
        [100, -10, 20, 10, 10, 20, -10, 100],
    ]

    def map_score(self):
        player_points = 0
        rival_points = 0

        for x in range(8):
            for y in range(8):
                if self.board.tiles[x][y] == self.agent_color:
                    player_points += self.WEIGHT_MAP[x][y]
                elif self.board.tiles[x][y] == self.rival_color:
                    rival_points += self.WEIGHT_MAP[x][y]
        return player_points - rival_points

    def heuristics_eval(self):
        movements_score_heuristic = self.movements_score()
        map_score_heuristic = self.map_score()
        final_heuristic = map_score_heuristic * 0.4 + movements_score_heuristic * 0.6
        return final_heuristic
