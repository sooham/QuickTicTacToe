class GameState:
    '''
    Snapshot of information between moves for a two-player, sequential move,
    zero-sum and perfect-information game.

    In the special case that the game is over, the next player is recorded,
    but may not make a legal move.

    player: str    -- The current player "p1" or "p2".
    over: bool          -- flag indicating whether game is over
    WIN: float          -- class constant indicating next player has won
    LOSE: float         -- class constant indicating next player has lost
    DRAW: float         -- class constant indicating next player tied
    '''
    # assign class constants
    WIN, LOSE, DRAW = 1.0, -1.0, 0.0

    def __init__(self, p):
        '''(GameState, str) -> NoneType

        Construct the starting state for an occurrence of the game with
        current player p.

        prerequisite - p is in {'p1', 'p2'}
        '''
        self.player = p
        self.over = False

    def apply_move(self, move):
        '''(GameState, Move) -> GameState

        Return the new game state reached by applying move to
        state self, or None if the move is illegal.
        '''
        raise NotImplementedError('Implement in a subclass')

    def opponent(self):
        '''(GameState) -> str

        Return the opponent of the next player, either 'p1' or 'p2'.

        >>> gs = GameState('p1')
        >>> gs.opponent()
        p2
        '''
        return 'p2' if self.player == 'p1' else 'p1'

    def outcome(self):
        ''' (GameState) -> float

        Return the outcome of this game state for self.player at end
        of game. The outcome is in {WIN, LOSE, DRAW}.

        self.over must be True.
        '''
        if self.winner(self.player):
            return GameState.WIN
        elif self.winner(self.opponent()):
            return GameState.LOSE
        else:
            return GameState.DRAW

    def possible_next_moves(self):
        ''' (GameState) -> list of Move

        Return a (possibly empty) list of moves that are legal
        from the present state.
        '''
        raise NotImplementedError('Implement in a subclass')

    def winner(self, player):
        ''' (GameState, str) -> bool

        Return whether player has won the game.

        Assume: player is either 'p1' or 'p2'
                and there are no more legal moves; the game is over
        '''
        raise NotImplementedError('Implement in a subclass')
