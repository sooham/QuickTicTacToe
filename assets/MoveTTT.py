from Move import Move


class MoveTTT(Move):
    '''
    A class that represents a move on the TicTacToe board

    position: (int, int) -- the coordinates on a TicTacToe board.
    '''

    def __init__(self, coordinates):
        ''' (MoveTTT, tuple of (int, int)) -> NoneType

        Initializes the MoveTTT instance (self) to act on the coordinates
        (coordinates)

        >>> move = MoveTTT((1,2))
        >>> move.position
        (1, 2)
        '''

        self.position = coordinates
