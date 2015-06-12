from GameState import GameState
from MoveTTT import MoveTTT

CIRCLE = "\u25EF"
CROSS = "\u292B"


class GameStateTTT(GameState):
    '''
    The state of TicTacToe Game.

    Stores information on the state of the TicTacToe board,
    and the player to move, if the game is over.

    Inherited:
        player: str         -- current player.
        over: bool          -- flag indicating whether game is over
        WIN: float          -- class constant indicating next player has won
        LOSE: float         -- class constant indicating next player has lost
        DRAW: float         -- class constant indicating next player tied

    New:
        board: dict tuple to str -- map from coordinates to value
        MAGICSQUARE: A 3x3 magic square used to check for winners
    '''

    MAGICSQUARE = {
        (0, 0): 8, (0, 1): 1, (0, 2): 6,
        (1, 0): 3, (1, 1): 5, (1, 2): 7,
        (2, 0): 4, (2, 1): 9, (2, 2): 2
        }

    def __init__(self, p, board=None):
        r'''(GameStateTTT, str, bool) -> NoneType

        Initializes GameStateTTT (self) with an empty TicTacToe (board) of
        with player (p).

        Prerequisite - p is in {'p1', 'p2'}
        Overridden from GameState.

        >>> game_state = GameStateTTT('p1' {(1,1): 'X'})
        >>> game_state.player
        'p1'
        >>> game_state.board
        {(1, 1): 'X'}
        >>> game_state.over
        False
        '''
        # The board is a dictionary mapping coordinate tuples to the
        # value in {CROSS, DOT}. This saves space.
        self.board = board if board else dict()
        GameState.__init__(p)

    def apply_move(self, move):
        r''' (GameStateTTT, MoveTTT) -> GameStateTTT

        Return the new game state reached after player applies (move) to
        (self). The return GameStateTTT contains the player's new action.

        Overridden from GameState.

        >>> gs1 = GameStateTTT('p1', {(1,1): 'O'})
        >>> move = MoveTTT((2,2))
        >>> gs2 = gs1.apply_move(move)
        >>> gs2.board
        "board={(1, 1): 'O', (2, 2): 'O'}"
        >>> gs2.player
        "p2"
        '''

        if move in self.possible_next_moves():
            new_board = dict(self.board)  # prevents aliasing
            new_board[move.position] = (
                CIRCLE if self.opponent() == 'p1' else CROSS)
            return GameStateTTT(self.opponent(), board=new_board)
        else:
            return None

    def possible_next_moves(self):
        r''' (GameStateTTT) -> list of MoveTTT

        Return a (possibly empty) list of moves that are legal for the
        current player from the present state (self).

        Overridden from GameState.
        '''
        if self.TTT_created():
            self.over = True
            return []

        available_pos = {
            (x, y) for y in range(2) for x in range(2)
        }
        # use sets to get the empty positions
        empty_pos = available_pos.difference(self.board)
        self.over = empty_pos == []
        return [MoveTTT(pos) for pos in empty_pos]

    def TTT_created(self):
        r''' (GameStateTTT) -> bool

        Return True iff a TicTacToe has been made on the game state's board.
        '''

        # overlay the magic square constants for each player, if the sum
        # of the positions is 15 or 30 then True
        if len(self.board) < 5:
            return False
        # check horizontals and verticals
        for row in range(2):
            row_sum = 0
            for col in range(2):
                if (col, row) not in self.board:
                    break
                const = 2 if self.board[(col, row) == CIRCLE] else 1
                row_sum += GameStateTTT.MAGICSQUARE[(col, row)] * const
            if row_sum == 15 or row_sum == 30:
                return True

        for col in range(2):
            col_sum = 0
            for row in range(2):
                if (col, row) not in self.board:
                    break
                const = 2 if self.board[(col, row) == CIRCLE] else 1
                col_sum += GameStateTTT.MAGICSQUARE[(col, row)] * const
            if col_sum == 15 or col_sum == 30:
                return True

        # check diagonal and anti-diagonal
        diag_sum = 0
        anti_diag_sum = 0
        for num in range(2):
            diag_sum += GameStateTTT.MAGICSQUARE[(num, num)] * const
            anti_diag_sum += GameState.MAGICSQUARE[(num, 2 - num)] * const

        if 15 in [diag_sum, anti_diag_sum] or 30 in [diag_sum, anti_diag_sum]:
            return True

        return False

    def winner(self, player):
        r''' (GameStateTTT, str) -> bool

        Return True iff the winner of the game_state (self) is the player
        (player). If game is not over return False.

        Precondition - player in {'p1', 'p2'}
        Overridden from GameState.

        '''

        # if we have reached a game over state with a TicTacToe then
        # the next player has lost
        return player != self.player if self.TTT_created() else False
