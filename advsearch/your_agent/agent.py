import random

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

    print(heuristic(the_board, color))
    return random.choice([(2, 3), (4, 5), (5, 4), (3, 2)])


def heuristic(the_board, color):
    """
    Retorna o numero de jogadas possiveis do oponente
    :return: int
    """
    # inicia em zero o numero de jogadas possiveis
    opponent_moves = 0

    # verifica qual a cor do jogador para pegar a do oponente
    opponent_color = 'B' if color == 'W' else 'W'

    # percorre o board buscando posicoes validas
    tiles = [(x, y) for x in range(8) for y in range(8)]
    for x, y in tiles:
        if(the_board.is_legal((x, y), opponent_color)):
            opponent_moves += 1

    # retorna o numero de jogadas possiveis
    return opponent_moves
