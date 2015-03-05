"""
NAME
    tic_tac_toe_move

DESCRIPTION
    This module contains the function for the move class data structure
    used in TTTGameState called TTTMove. TTTMove is basically the
    object representation of a move done by the player.


CLASSES
    move
    move.Move
        TTTMove
"""


class Move:

    ''' A move in a two-player, sequential move,
    zero-sum, perfect-information game.
    '''
    
    # definition complete


class TTTMove(Move):
    '''
    A class that represents a move on the tic tac toe board

    position: (int, int) -- the coordinates on a tic tac toe board the move affects.
    '''

    def __init__(self, coordinates):
        ''' (TTTMove, tuple of (int, int)) -> NoneType

        Initialises the TTTMove instance (self) to act on the coordinates
        (coordinates)

        >>> move = TTTMove((1,2))
        >>> move.position
        (1, 2)
        '''

        self.position = coordinates

    def __eq__(self, other):
        ''' (self, object) -> bool

        Return True if and only if other is an instance of the class TTTMove
        and other has the same position instance variable.

        >>> move1 = TTTMove((1, 2))
        >>> move2 = TTTMove((3, 4))
        >>> move3 = TTTMove((3, 4))
        >>> move2 is move3
        False
        >>> move2 == move3
        True
        >>> move2 == move1
        False
        '''

        return isinstance(other, TTTMove) and self.position == other.position

    def __str__(self):
        ''' (self) -> str

        Return a human readable string representation of (self)

        >>> move1 = TTTMove((100, 0))
        >>> str(move1)
        '(100, 0)'
        '''

        return str(self.position)

    def __repr__(self):
        ''' (self) -> str

        Return the python interpretable string representation of (self)

        >>> move1 = TTTMove((1, 12))
        >>> repr(move1)
        'TTTMove((1, 12))'
        >>> move2 = eval(repr(move1))
        >>> move1 == move2
        True
        '''

        return 'TTTMove({})'.format(self.position)
