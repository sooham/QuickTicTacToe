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

    def __eq__(self, other):
        ''' (self, object) -> bool

        Return True if and only if other is an instance of the class MoveTTT
        and other has the same position instance variable.

        >>> move1 = TippyMove((1, 2))
        >>> move2 = TippyMove((3, 4))
        >>> move3 = TippyMove((3, 4))
        >>> move2 is move3
        False
        >>> move2 == move3
        True
        >>> move2 == move1
        False
        '''

        return isinstance(other, MoveTTT) and self.position == other.position
