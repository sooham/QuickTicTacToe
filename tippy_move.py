"""
NAME
    tippy_move

DESCRIPTION
    This module contains the function for the move class data structure
    used in TippyGameState called TippyMove. TippyMove is basically the
    object representation of a move done by the player.


CLASSES
    move.Move
        TippyMove
"""

from move import Move


class TippyMove(Move):
    '''
    A class that represents a move on the tippy board

    position: (int, int) -- the coordinates on a tippy board the move affects.
    '''

    def __init__(self, coordinates):
        ''' (TippyMove, tuple of (int, int)) -> NoneType

        Initialises the TippyMove instance (self) to act on the coordinates
        (coordinates)

        >>> move = TippyMove((1,2))
        >>> move.position
        (1, 2)
        '''

        self.position = coordinates

    def __eq__(self, other):
        ''' (self, object) -> bool

        Return True if and only if other is an instance of the class TippyMove
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

        return isinstance(other, TippyMove) and self.position == other.position

    def __str__(self):
        ''' (self) -> str

        Return a human readable string representation of (self)

        >>> move1 = TippyMove((100, 0))
        >>> str(move1)
        '(100, 0)'
        '''

        return str(self.position)

    def __repr__(self):
        ''' (self) -> str

        Return the python interpretable string representation of (self)

        >>> move1 = TippyMove((1, 12))
        >>> repr(move1)
        'TippyMove((1, 12))'
        >>> move2 = eval(repr(move1))
        >>> move1 == move2
        True
        '''

        return 'TippyMove({})'.format(self.position)
