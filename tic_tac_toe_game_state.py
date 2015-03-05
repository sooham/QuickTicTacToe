"""
NAME
    tippy_game_state

DESCRIPTION
    This module contains the game state for the game tippy
    subclassed from game_state. The class described here helps
    render and represent the tippy board.

FUNCTIONS
    input_coordinates
    str_tippy_board

CLASSES
    game_state.GameState
        TippyGameState

CONSTANTS
    DOT
    CROSS
    CIRCLE
    TippyGameState.TIPPIES_GRID
"""

from game_state import GameState
from tippy_move import TippyMove


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


def str_tippy_board(board, n):
    r''' (dict of coordinates: str, int) -> str

    Return the string representation of the tippy board (board) of
    dimension (n) x (n).

    >>> board_config = {(1, 1): 'X', (2, 2): 'O', (0,1): 'O'}
    >>> str_tippy_board(board_config, 3)[:50]
    '      0    1    2  \n\n 0    .    .    .  \n\n 1  OX  '

    '''

    # Notice the doctest only checks the first 50 characters
    # of each result. This is in order to keep the lines short,
    # as splitting lines with newline characters in a doctest
    # is not possible.

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


class TippyGameState(GameState):
    '''
    The state of the Tippy Game.

    Stores information on the dimension and state of the tippy board,
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
        TIPPIES_GRID: list of list of tuple (int, int) -- see below comment
    '''

    # TIPPIES_GRID holds the pattern of the main two reflected tippes
    # for tippy detection purposes, see self.tippy_created()
    TIPPIES_GRID = [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (-1, 0), (-1, 1), (-2, 1)]
    ]

    def __init__(self, p, interactive=False, board=None, n=None):
        r'''(TippyGameState, str, bool) -> NoneType

        Initialises TippyGameState (self) with an empty tippy (board) of
        dimensions (n) x (n) and next player (p).
        If (interactive) prompt for input.

        Prerequisite - p is in {'p1', 'p2'}
        Overriden from GameState.

        >>> game_state = TippyGameState('p1', False, {(1,1): 'X'}, 15)
        >>> game_state.next_player
        'p1'
        >>> game_state.board
        {(1, 1): 'X'}
        >>> game_state.n
        15
        >>> game_state.instructions
        'To win the game you have to make a tippy in any orientation.'
        >>> game_state.over
        False
        '''

        # cannot display the case where the n input is ommitted in
        # the doctest as that would invoke call on input()

        if not n:
            # set the dimension of tippy board, avoid TypeError
            successful_entry = False
            while not successful_entry:
                try:
                    self.n = int(input(
                        'Enter the width of the square grid: '))
                    if self.n < 3:
                        raise ValueError
                    successful_entry = True
                except:
                    print("Not a vaild number (must be at least three),")
        else:
            self.n = n

        # The board is a dictionary mapping coordinate tuples to the
        # value in {CROSS, DOT}. This not only saves space, but allows
        # for easy manipulations to detect a tippy.

        self.board = board if board else dict()
        self.instructions = ('To win the game you have to make a tippy in'
                             ' any orientation.')
        self.next_player = p
        self.over = False

    def __eq__(self, other):
        r''' (TippyGameState, object) -> bool

        Return True iff (other) is an instance of TippyGameState and
        (self) and (other) have the same n and board instance variables.

        >>> gs1 = TippyGameState('p1', False, {}, 3)
        >>> gs2 = TippyGameState('p2', True, {}, 3)
        >>> gs1 == gs2
        True
        >>> gs3 = TippyGameState('p1', True, {(1,1): CROSS}, 3)
        >>> gs1 == gs3
        False
        >>> gs4 = TippyGameState('p1', True, {(1,1): CROSS}, 4)
        >>> gs3 == gs4
        False
        >>> gs5 = int('2')
        >>> gs5 == gs1
        False
        '''

        return isinstance(other, TippyGameState) and (
            [other.n, other.board] == [self.n, self.board])

    def __repr__(self):
        r''' (TippyGameState) -> str

        Return the python interpretable representation of (self)

        >>> gs1 = TippyGameState('p1', False, {(1,1): 'O'}, 3)
        >>> repr(gs1)
        "TippyGameState(p1, board={(1, 1): 'O'}, n=3)"
        '''

        return 'TippyGameState({}, board={}, n={})'.format(
            self.next_player, self.board, self.n)

    def __str__(self):
        r'''(TippyGameState) -> str

        Return a string representation of the current TippyGameState (self).

        >>> board_config = { \
        ... (1, 1): CROSS, \
        ... (2, 2): CIRCLE, \
        ... (0, 1): CIRCLE \
        ... }
        >>> gs = TippyGameState('p1', False, board_config, 3)
        >>> str(gs).replace(DOT, "  .  ") \
        ... .replace(CIRCLE, "  O  ") \
        ... .replace(CROSS, "  X  ")[:50]
        '\n\n      0    1    2  \n\n 0    .    .    .  \n\n 1    '
        >>> gs2 = TippyGameState('p2', False, board_config, 3)
        >>> str(gs2).replace(DOT, "  .  ") \
        ... .replace(CIRCLE, "  O  ") \
        ... .replace(CROSS, "  X  ")[:50]
        '\n\n      0    1    2  \n\n 0    .    .    .  \n\n 1    '
        '''

        # Notice the doctest only checks the first 50 characters
        # of each result. This is in order to keep the lines short,
        # as splitting lines with newline characters in a doctest
        # is not possible.

        result = '\n\n' + str_tippy_board(self.board, self.n)
        result += ('\n\nNext player is computer'
                   if self.next_player == 'p1' else '')
        return result

    def apply_move(self, move):
        r''' (TippyGameState, TippyMove) -> TippyGameState

        Return the new TippyGameState reached after player applies (move) to
        (self). The return TippyGameState contains the player's new action.

        Overriden from GameState.

        >>> gs1 = TippyGameState('p1', False, {(1,1): 'O'}, 3)
        >>> repr(gs1)
        "TippyGameState(p1, board={(1, 1): 'O'}, n=3)"
        >>> move = TippyMove((2,2))
        >>> gs2 = gs1.apply_move(move)
        >>> repr(gs2).replace(CIRCLE, 'O')
        "TippyGameState(p2, board={(1, 1): 'O', (2, 2): 'O'}, n=3)"
        >>> move = TippyMove((100,0))
        >>> gs3 = gs1.apply_move(move)
        >>> gs3 == None
        True
        '''

        if move in self.possible_next_moves():
            new_board = dict(self.board)  # prevents aliasing
            new_board[move.position] = (
                CROSS if self.opponent() == 'p1' else CIRCLE)
            return TippyGameState(self.opponent(), board=new_board, n=self.n)
        else:
            return None

    def get_move(self):
        r''' (TippyGameState) -> TippyMove

        The GameState (self) return a TippyMove (move) by prompting the
        user. Overriden from GameState.
        '''
        # No doctest as function uses input() indirectly
        return TippyMove(input_coordinates('Enter a coordinate X, Y: '))

    def possible_next_moves(self):
        r''' (TippyGameState) -> list of TippyMove

        Return a (possibly empty) list of moves that are legal for the
        current player from the present state (self).

        Overriden from GameState.

        >>> gs1 = TippyGameState('p1', False, {(1,1):CIRCLE}, 2)
        >>> repr(gs1.possible_next_moves())
        '[TippyMove((0, 1)), TippyMove((1, 0)), TippyMove((0, 0))]'
        >>> gs2 = TippyGameState('p2', False, {(1,1):CIRCLE,
        ... (0,0):CIRCLE, (0,1):CIRCLE, (1,2):CIRCLE}, 3)
        >>> gs2.possible_next_moves()
        []
        '''
        # The above doctest will render incorrect for some machines
        # depending on wether it can support unicode characters or not.

        # Game rules state:
        # if a tippy has been created then no moves can be made
        # a player cannot move on a position that is filled or is not on the
        # board
        if self.tippy_created():
            self.over = True
            return []
        # else
        available_pos = {
            (x, y) for y in range(self.n) for x in range(self.n)
        }
        # use sets to get the empty positions
        empty_pos = available_pos.difference(self.board)
        self.over = empty_pos == []
        return [TippyMove(pos) for pos in empty_pos]

    def tippy_threshold(self, position, tippy, direction=1, threshold=2):
        r''' (TippyGameState, tuple of int, list of tuple, int, int) -> float

        Return 1.0 if self.next_player can create a tippy (tippy) starting at
        position with format (x, y), with a direction of 1, or -1 (reflected),
        in less than or equal to [4 - threshold] moves. Else return -1.0 if
        self.opponent() can create a tippy with the same specifications,
        else return 0.0.

        >>> game_state = TippyGameState("p1", False, {
        ... (0, 0): CROSS,
        ... (1, 0): CROSS,
        ... (2, 0): CIRCLE,
        ... (0, 1): CIRCLE,
        ... (2, 2): CIRCLE
        ... }, 3)
        >>> game_state.tippy_threshold(
        ... (0, 0),
        ... TippyGameState.TIPPIES_GRID[0]
        ... )
        1.0
        >>> game_state.tippy_threshold(
        ... (1,0),
        ... TippyGameState.TIPPIES_GRID[0]
        ... )
        0.0
        >>> game_state.tippy_threshold(
        ... (0,1),
        ... TippyGameState.TIPPIES_GRID[0]
        ... )
        -1.0
        '''
        # Check if at least 3 out of 4 cells of tippy are found
        x, y = position
        success_measure = 0
        success_player = None
        for tippy_cell in tippy:
            tippy_cell = (
                x + (direction * tippy_cell[0]),
                y + (direction * tippy_cell[1])
            )
            if tippy_cell in self.board:
                board_tippy_cell = self.board[tippy_cell]
                # If tippy is being created by same player
                # Add to success_measure
                if not success_player:
                    success_player = board_tippy_cell
                if board_tippy_cell == success_player:
                    success_measure += 1
                else:
                    return 0.0
        if success_measure >= threshold:
            return (1.0
                    if success_player == (
                        CIRCLE if self.next_player == "p2"
                        else CROSS
                    ) else -1.0)
        return 0.0

    def rough_outcome(self):
        r''' (TippyGameState) -> int

        Return an estimate in interval [LOSE, WIN] of best outcome next_player
        can guarantee from state (self). Overriden from GameState.

        >>> game_state = TippyGameState("p1", False, {
        ... (0, 0): CROSS,
        ... (1, 0): CROSS,
        ... (2, 0): CIRCLE,
        ... (0, 1): CIRCLE
        ... }, 3)
        >>> game_state.rough_outcome()
        1.0
        >>> game_state2 = TippyGameState("p1", False, {
        ... (0, 0): CROSS,
        ... (1, 0): CROSS,
        ... (2, 0): CIRCLE,
        ... (0, 1): CIRCLE,
        ... (1, 1): CIRCLE
        ... }, 3)
        >>> game_state2.rough_outcome()
        -1.0
        >>> game_state3 = TippyGameState("p1", False, {
        ... (2, 0): CIRCLE,
        ... (1, 1): CROSS,
        ... (2, 0): CIRCLE
        ... }, 3)
        >>> game_state3.rough_outcome()
        0.0
        '''
        # Notice that the return values are hardcoded into the docstring
        # Because it is not possible to compare them to a variable
        # (Namely TippyGameState.WIN or similar)

        # Go through positions that have been filled
        for x, y in self.board:
            for tippy in self.TIPPIES_GRID:
                # Check if at least 2 out of 4 cells of tippy are found
                tippy1 = self.tippy_threshold((x, y), tippy)
                if(tippy1 == 1.0):
                    return TippyGameState.WIN
                elif(tippy1 == -1.0):
                    return TippyGameState.LOSE
                # Check for reverse tippy, same as above
                tippy2 = self.tippy_threshold((x, y), tippy, -1)
                if(tippy2 == 1.0):
                    return TippyGameState.WIN
                elif(tippy2 == -1.0):
                    return TippyGameState.LOSE
        return TippyGameState.DRAW

    def tippy_created(self):
        r''' (TippyGameState) -> bool

        Return True iff a tippy has been made on the (self) game state's board.

        >>> gs = TippyGameState('p2', False, {
        ... (1, 1): CIRCLE,
        ... (0, 0): CIRCLE,
        ... (0, 1): CIRCLE,
        ... (1, 2): CIRCLE
        ... }, 3)
        >>> gs.tippy_created()
        True
        >>> gs2 = TippyGameState('p2', False, {(1, 1): CIRCLE}, 3)
        >>> gs2.tippy_created()
        False
        >>> gs3 = TippyGameState('p2', False, {
        ... (1, 1): CIRCLE,
        ... (0, 0): CIRCLE,
        ... (1, 0): CIRCLE,
        ... (2, 1): CIRCLE
        ... }, 3)
        >>> gs3.tippy_created()
        True
        '''

        # The most efficient way of detecting a tippy
        # 1. iterate through every filled poisiton in self.board
        # 2. check if any of the positions adjacent to the spot are occupied
        # 3. if # 2 is true check that for every tippy position in TIPPY_GRID
        #    that the relative position is occupied
        # 4. repeat 1 - 3 with the transpose of the board coorinates

        transpose = {coord[::-1]: mark for (coord, mark) in self.board.items()}
        adjacents = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for x, y in self.board:
            has_adjacents = any([((x + dx, y + dy) in self.board)
                                for dx, dy in adjacents])
            if has_adjacents:
                # check for tippy allotropes in the board and transpose board
                for tippy in TippyGameState.TIPPIES_GRID:
                    horizontal_tippy = any(
                        [all([((x + dx, y + dy), mark)
                         in self.board.items() for dx, dy in tippy])
                         for mark in [CIRCLE, CROSS]])

                    vertical_tippy = any(
                        [all([((y + dx, x + dy), mark)
                         in transpose.items() for dx, dy in tippy])
                         for mark in [CIRCLE, CROSS]])

                    if horizontal_tippy or vertical_tippy:
                        return True
        return False

    def winner(self, player):
        r''' (TippyGameState, str) -> bool

        Return True iff the winner of the game_state (self) is the player
        (player). If game is not over return False

        Precondition - player in {'p1', 'p2'}
        Overriden from GameState.

        >>> gs = TippyGameState('p2', False, {
        ... (1, 1): CIRCLE,
        ... (0, 0): CIRCLE,
        ... (0, 1): CIRCLE,
        ... (1, 2): CIRCLE
        ... }, 3)
        >>> gs.tippy_created()
        True
        >>> gs.winner('p1')
        True
        >>> gs2 = TippyGameState('p2', False, {(1, 1): CIRCLE}, 3)
        >>> gs2.tippy_created()
        False
        >>> gs2.winner('p1')
        False
        >>> gs2.winner('p2')
        False
        '''

        # if we have reached a game over state with a tippy then
        # the next player has lost
        return player != self.next_player if self.tippy_created() else False


# test if fancy charset for tippy works
try:
    print('Checking if character set works...')
    DOT = '  \u2022  '
    CIRCLE = '  \u25EF  '
    CROSS = '  \u292B  '
    print(DOT)
    print(CIRCLE)
    print(CROSS)
    print('Check successful!\n')
except:
    print('Test failed, Using normal charset :(')
    DOT = '  .  '
    CIRCLE = '  O  '
    CROSS = '  X  '
