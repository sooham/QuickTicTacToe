"""
NAME
    tic_tac_toe_game_state

DESCRIPTION
    This module contains the game state for the game tic tac toe
    subclassed from game_state. The class described here helps
    render and represent the tic tac toe board.

FUNCTIONS
    input_coordinates
    str_tic_tac_toe_board

CLASSES
    game_state.GameState
        TTTGameState

CONSTANTS
    DOT
    CROSS
    CIRCLE
"""
import itertools
from game_state import GameState
from tic_tac_toe_move import TTTMove


def input_coordinates(prompt):
    r''' (str) -> tuple of int

    Return the coordinates input by the user with prompt message (prompt).

    '''
    # Doctest for this function not possible as the function uses input()

    successful_entry = False    # To check if input is the correct Type
    while not successful_entry:
        # Prevent incorrect inputs from crashing program
        try:
            result = tuple(
                int(i) for i in input(prompt).split(',', 1))
            successful_entry = True
        except:
            print('Input must be format X, Y!\n')

    return result


def str_ttt_board(board, n):
    r''' (dict of coordinates: str, int) -> str

    Return the string representation of the tic tac toe board (board) of
    dimension (n) x (n).

    >>> board_config = {(1, 1): 'X', (2, 2): 'O', (0,1): 'O'}
    >>> str_tic_tac_toe_board(board_config, 3)[:50]
    '      0    1    2  \n\n 0    .    .    .  \n\n 1  OX  '

    '''

    # build the board row by row filling in all unoccupied positions
    # with the filler character DOT

    # The header row contains the coordinates of the column positions
    header_row = '    '
    header_row += ''.join([str(i).center(5) for i in range(n)])
    header_row += '\n\n'
    rows = []
    for y in range(n):
        row = str(y).center(4)  # adds the row's coordinates at beginning
        for x in range(n):
            # check if the coordinate (x,y) is occupied or fill
            row += board.get((x, y), DOT)
        rows.append(row)

    return header_row + '\n\n'.join(rows)


class TTTGameState(GameState):
    '''
    The state of the Tic Tac Toe Game.

    Stores information on the dimension and state of the tic tac toe board,
    and the next_payer to move, if the game is over.

    Inherited:
        next_player: str    -- player about to move, unless game is over
                               in which case it is the opponent of the player
                               who just moved
        over: bool          -- flag indicating whether game is over
        instructions: str   -- description of what actions to take at each turn
        WIN: float          -- class constant indicating next player has won
        LOSE: float         -- class constant indicating next player has lost
        DRAW: float         -- class constant indicating next player tied

    New:
        n: int                  -- dimensions of the board
        board: dict {tuple:str} -- dict from coordinates to the value there
    '''

    def __init__(self, p, interactive=False, board=None, n=None):
        r'''(TTTGameState, str, bool) -> NoneType

        Initialises TTTGameState (self) with an empty tic tac toe (board) of
        dimensions (n) x (n) and next player (p).
        If (interactive) prompt for input.

        Prerequisite - p is in {'p1', 'p2'}
        Overriden from GameState.

        >>> game_state = TTTGameState('p1', False, {(1,1): 'X'}, 15)
        >>> game_state.next_player
        'p1'
        >>> game_state.board
        {(1, 1): 'X'}
        >>> game_state.n
        15
        >>> game_state.instructions
        'To win the game you have to make a tic tac toe in any orientation.'
        >>> game_state.over
        False
        '''

        # The board is a dictionary mapping coordinate tuples to the
        # value in {CROSS, DOT}. This not only saves space, but allows
        # for easy manipulations to detect a tic tac toe.
        self.n = n
        self.board = board if board else dict()
        self.instructions = 'Welcome to Tic Tac Toe!'
        self.next_player = p
        self.over = False

    def __eq__(self, other):
        r''' (TTTGameState, object) -> bool

        Return True iff (other) is an instance of TTTGameState and
        (self) and (other) have the same n and board instance variables.

        >>> gs1 = TTTGameState('p1', False, {}, 3)
        >>> gs2 = TTTGameState('p2', True, {}, 3)
        >>> gs1 == gs2
        True
        >>> gs3 = TTTGameState('p1', True, {(1,1): CROSS}, 3)
        >>> gs1 == gs3
        False
        >>> gs4 = TTTGameState('p1', True, {(1,1): CROSS}, 4)
        >>> gs3 == gs4
        False
        >>> gs5 = int('2')
        >>> gs5 == gs1
        False
        '''

        return isinstance(other, TTTGameState) and (
            [other.n, other.board] == [self.n, self.board])

    def __repr__(self):
        r''' (TTTGameState) -> str

        Return the python interpretable representation of (self)

        >>> gs1 = TTTGameState('p1', False, {(1,1): 'O'}, 3)
        >>> repr(gs1)
        "TTTGameState(p1, board={(1, 1): 'O'}, n=3)"
        '''

        return 'TTTGameState({}, board={}, n={})'.format(
            self.next_player, self.board, self.n)

    def __str__(self):
        r'''(TTTGameState) -> str

        Return a string representation of the current TTTGameState (self).

        >>> board_config = { \
        ... (1, 1): CROSS, \
        ... (2, 2): CIRCLE, \
        ... (0, 1): CIRCLE \
        ... }
        >>> gs = TTTGameState('p1', False, board_config, 3)
        >>> str(gs).replace(DOT, "  .  ") \
        ... .replace(CIRCLE, "  O  ") \
        ... .replace(CROSS, "  X  ")[:50]
        '\n\n      0    1    2  \n\n 0    .    .    .  \n\n 1    '
        >>> gs2 = TTTGameState('p2', False, board_config, 3)
        >>> str(gs2).replace(DOT, "  .  ") \
        ... .replace(CIRCLE, "  O  ") \
        ... .replace(CROSS, "  X  ")[:50]
        '\n\n      0    1    2  \n\n 0    .    .    .  \n\n 1    '
        '''

        # Notice the doctest only checks the first 50 characters
        # of each result. This is in order to keep the lines short,
        # as splitting lines with newline characters in a doctest
        # is not possible.

        result = '\n\n' + str_ttt_board(self.board, self.n)
        result += ('\n\nNext player is computer'
                   if self.next_player == 'p1' else '')
        return result

    def apply_move(self, move):
        r''' (TTTGameState, TTTMove) -> TTTGameState

        Return the new TTTGameState reached after player applies (move) to
        (self). The return TTTGameState contains the player's new action.

        Overriden from GameState.

        >>> gs1 = TTTGameState('p1', False, {(1,1): 'O'}, 3)
        >>> repr(gs1)
        "TTTGameState(p1, board={(1, 1): 'O'}, n=3)"
        >>> move = TTTMove((2,2))
        >>> gs2 = gs1.apply_move(move)
        >>> repr(gs2).replace(CIRCLE, 'O')
        "TTTGameState(p2, board={(1, 1): 'O', (2, 2): 'O'}, n=3)"
        >>> move = TTTMove((100,0))
        >>> gs3 = gs1.apply_move(move)
        >>> gs3 == None
        True
        '''

        if move in self.possible_next_moves():
            new_board = dict(self.board)  # prevents aliasing
            new_board[move.position] = (
                CROSS if self.opponent() == 'p1' else CIRCLE)
            return TTTGameState(self.opponent(), board=new_board, n=self.n)
        else:
            return None

    def get_move(self):
        r''' (TTTGameState) -> TTTMove

        The GameState (self) return a TTTMove (move) by prompting the
        user. Overriden from GameState.
        '''
        # No doctest as function uses input() indirectly
        return TTTMove(input_coordinates('Enter a coordinate X, Y: '))

    def possible_next_moves(self):
        r''' (TTTGameState) -> list of TTTMove

        Return a (possibly empty) list of moves that are legal for the
        current player from the present state (self).

        Overriden from GameState.

        >>> gs1 = TTTGameState('p1', False, {(1,1):CIRCLE}, 2)
        >>> repr(gs1.possible_next_moves())
        '[TTTMove((0, 1)), TTTMove((1, 0)), TTTMove((0, 0))]'
        >>> gs2 = TTTGameState('p2', False, {(1,1):CIRCLE,
        ... (0,0):CIRCLE, (0,1):CIRCLE, (1,2):CIRCLE}, 3)
        >>> gs2.possible_next_moves()
        []
        '''
        # The above doctest will render incorrect for some machines
        # depending on wether it can support unicode characters or not.

        # Game rules state:
        # if a tic tac toe has been created then no moves can be made
        # a player cannot move on a position that is filled or is not on the
        # board
        if self.ttt_created():
            self.over = True
            return []
        # else
        available_pos = {
            (x, y) for y in range(self.n) for x in range(self.n)
        }
        # use sets to get the empty positions
        empty_pos = available_pos.difference(self.board)
        self.over = empty_pos == []
        return [TTTMove(pos) for pos in empty_pos]

    def ttt_created(self):
        r''' (TTTGameState) -> bool

        Return True iff a tic tac toe has been made on the (self) game state's board.

        >>> gs = TTTGameState('p2', False, {
        ... (1, 1): CIRCLE,
        ... (0, 0): CIRCLE,
        ... (0, 1): CIRCLE,
        ... (1, 2): CIRCLE
        ... }, 3)
        >>> gs.ttt_created()
        True
        >>> gs2 = TTTGameState('p2', False, {(1, 1): CIRCLE}, 3)
        >>> gs2.ttt_created()
        False
        >>> gs3 = TTTGameState('p2', False, {
        ... (1, 1): CIRCLE,
        ... (0, 0): CIRCLE,
        ... (1, 0): CIRCLE,
        ... (2, 1): CIRCLE
        ... }, 3)
        >>> gs3.ttt_created()
        True
        '''

        # The most efficient way of detecting a tic tac toe win
        # 1. Check if any at least two of the corners of the board is filled
        # 2. Check that the middle postion is filled

        sides = [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (2, 2), (1, 2), (2, 1)]

        # check if at least two corner positions are filled
        for position in sides[:]:
            if position not in self.board:
                sides.remove(position)

        if len(sides) > 1:
            # get the cartesian product of all the filled corners
            for a, b in itertools.product(sides, sides):
                if a != b:
                    # check if the averge of the two is occupied
                    c = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                    if c in self.board:
                        if self.board[a] == self.board[b] == self.board[c]:
                            return True
        return False

    def winner(self, player):
        r''' (TTTGameState, str) -> bool

        Return True iff the winner of the game_state (self) is the player
        (player). If game is not over return False

        Precondition - player in {'p1', 'p2'}
        Overriden from GameState.

        >>> gs = TTTGameState('p2', False, {
        ... (1, 1): CIRCLE,
        ... (0, 0): CIRCLE,
        ... (0, 1): CIRCLE,
        ... (1, 2): CIRCLE
        ... }, 3)
        >>> gs.ttt_created()
        True
        >>> gs.winner('p1')
        True
        >>> gs2 = TTTGameState('p2', False, {(1, 1): CIRCLE}, 3)
        >>> gs2.ttt_created()
        False
        >>> gs2.winner('p1')
        False
        >>> gs2.winner('p2')
        False
        '''

        # if we have reached a game over state with a tic tac toe then
        # the next player has lost
        return player != self.next_player if self.ttt_created() else False


# test if fancy charset for tic tac toe works
try:
    DOT = '  \u2022  '
    CIRCLE = '  \u25EF  '
    CROSS = '  \u292B  '
    print(DOT, CIRCLE, CROSS, '...')
except:
    DOT = '  .  '
    CIRCLE = '  O  '
    CROSS = '  X  '
