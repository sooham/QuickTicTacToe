"""
NAME
    strategy_minimax_memoize

DESCRIPTION
    StrategyMinimaxMemoize is an efficient implementation of the traditional
    minimax algorithm with additional memoization capabilities. This class
    is subclassed from the generic Strategy class.

CLASSES
    strategy.Strategy
        StrategyMinimaxMemoize
"""

import random
from strategy import Strategy


class StrategyMinimaxMemoize(Strategy):
    '''
    A faster implementation of minimax with memoization capabilities.
    Use a GameState (or it's subclass) to find and return the most
    optimal move for the the current_player to win or draw.

    Inherits from Strategy

    Instance Variables:
        memo: dict of (str: int)    -- This is the dictionary used to store
                                    the memoization results. The keys in the
                                    dictionary are the __repr__ strings for the
                                    GameState and the values are respective
                                    player outcome from minimax {-1, 0, 1}.

    Methods:
        - suggest_move: return a move that leads to the best
            predicted outcome.
    '''

    def __init__(self, interactive=False):
        ''' (StrategyMinimaxMemoize, bool) -> NoneType
        Initialize new instance of StrategyMinimaxMemoize called (self) with
        interactive capabilities.

        >>> strategy = StrategyMinimaxMemoize()
        >>> strategy.memo
        {}
        '''

        # Extend Strategy
        Strategy.__init__(self, interactive)
        self.memo = {}

    def __eq__(self, other):
        ''' (StrategyMinimaxMemoize, object) -> bool

        Return True iff (other) is of the same instance as (self).

        >>> strategy = StrategyMinimaxMemoize()
        >>> better_strategy = StrategyMinimaxMemoize()
        >>> better_strategy == strategy
        True
        >>> better_strategy == 1.0
        False
        '''

        return isinstance(other, StrategyMinimaxMemoize)

    def __repr__(self):
        ''' (StrategyMinimaxMemoize) -> str

        Return a python interpretable string representing (self).

        >>> repr(StrategyMinimaxMemoize())
        'StrategyMinimaxMemoize()'
        '''

        return 'StrategyMinimaxMemoize()'

    def __str__(self):
        ''' (StrategyMinimaxMemoize) -> str

        Return a human interpretable string representing (self).

        >>> str(StrategyMinimaxMemoize())
        'A Memoized Minimax Strategy Class'
        '''

        return 'A Memoized Minimax Strategy Class'

    def suggest_move(self, game_state, root=True):
        r''' (StrategyMinimaxMemoize, GameState, bool) -> Move

        (self) return a move that allows game_state.next_player to choose
        the most beneficial move. The (root) parameter will return a move
        if True, or the numerical score for the game {-1, 0, 1} if set as
        False.

        Overrides Strategy.suggest_move

        >>> from subtract_square_state import SubtractSquareState
        >>> game_state = SubtractSquareState('p1', False, 8)
        >>> game_strategy = StrategyMinimaxMemoize()
        >>> game_strategy.suggest_move(game_state).amount
        1
        '''

        # Check if the value for the game_state is stored in the
        # memoization dictionary

        if repr(game_state) in self.memo:
            # return the value for the game_state without calculations
            return self.memo[repr(game_state)]

        # otherwise
        # memoize and return the game_state and resulting values
        # handle the case when root == True for returning a Move class

        available_moves = game_state.possible_next_moves()
        if available_moves:
            # make a list of the child game states
            children = [
                game_state.apply_move(move) for move in available_moves
            ]
            # get the minimax of the opponents final score forall child
            # game states and multiply by -1
            scores_list = [-1 * self.suggest_move(
                child, False) for child in children]
            score = max(scores_list)

            if root:
                # we want to return a Move object with the highest score
                return_moves = [available_moves[i] for i in range(
                    len(available_moves)) if scores_list[i] == score]
                return random.choice(return_moves)
            else:
                # we're still computing minimax
                # memoize the score for this game_state and return
                self.memo[repr(game_state)] = score
                return score
        else:  # BASE CASE
            # there are no moves, hence the game has ended
            # memoize and return the next_players outcome for the game
            self.memo[repr(game_state)] = game_state.outcome()
            return game_state.outcome()
