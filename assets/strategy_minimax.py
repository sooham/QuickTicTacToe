"""
NAME
    strategy_minimax

DESCRIPTION
    This module contains the implementation of the minimax strategy
    used by the StrategyMinimax class. Minimax is a strategy crucial
    to make a strong AI.

FUNCTIONS
    minimax

CLASSES
    strategy.Strategy
        StrategyMinimax
"""

import random
from strategy import Strategy


class StrategyMinimax(Strategy):
    '''
    The strong strategy min and max.

    Uses the state of a game to predict the best possible strategy
    by calculating all autcomes on each move.

    Inherits Strategy.

    Methods:
        - suggest_move: return a move that leads to the best
            predicted outcome.

    '''

    # No need for __init__ as this class has no instance variables

    def __eq__(self, other):
        ''' (StrategyMinimax, object) -> bool

        Return True iff (other) is of the same instance as (self)

        >>> strategy = StrategyMinimax()
        >>> better_strategy = StrategyMinimax()
        >>> better_strategy == strategy
        True
        >>> better_strategy == 1.0
        False
        '''

        return isinstance(other, StrategyMinimax)

    def __repr__(self):
        ''' (StrategyMinimax) -> str

        Return a python interpretable string representing (self).

        >>> repr(StrategyMinimax())
        'StrategyMinimax()'
        '''

        return 'StrategyMinimax()'

    def __str__(self):
        ''' (StrategyMinimax) -> str

        Return a human interpretable string representing (self).

        >>> str(StrategyMinimax())
        'Minimax Strategy Class'
        '''

        return 'Minimax Strategy Class'

    def suggest_move(self, game_state, root=True):
        r''' (StrategyMinimax, GameState, bool) -> Move

        (self) return a move that lets game_state.next_player most likely to
        win current game_state.(root) parameter will return a move if set
        true or the bool represntaion of the best move if False.

        Overrides Strategy.suggest_move

        >>> from subtract_square_state import SubtractSquareState
        >>> game_state = SubtractSquareState('p1', False, 8)
        >>> game_strategy = StrategyMinimax()
        >>> game_strategy.suggest_move(game_state).amount
        1
        '''

        # get the available moves for current game_state
        available_moves = game_state.possible_next_moves()
        if available_moves:
            # make a list of the child game states
            children = [
                game_state.apply_move(move) for move in available_moves
            ]
            # get the minimax of the opponents final score in child game states
            # multiplying by -1 will give you the current player's score
            scores_list = [-1 * self.suggest_move(
                child, False) for child in children]
            score = max(scores_list)
            if root:
                # then we want to return a Move object with the highest score
                return_moves = [available_moves[i] for i in range(
                    len(available_moves)) if scores_list[i] == score]
                return random.choice(return_moves)
            else:
                # we're still in the computing minimax, return the final
                # score of game_state
                return score
        else:
            # there are no moves, hence the game has ended
            # return the next_players outcome of the game
            return game_state.outcome()
