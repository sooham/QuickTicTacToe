"""
NAME
    strategy_minimax_myopic

DESCRIPTION
    This module contains the implementation of StrategyMinimaxMyopic,
    a faster but cruder implementation of minimax using the rough_outcome
    heuristic.

FUNCTIONS
    minimax

CLASSES
    strategy.Strategy
        StrategyMinimaxMyopic
"""

import random
from strategy import Strategy


class StrategyMinimaxMyopic(Strategy):
    '''
        A faster implementation for minimax, called StrategyMinimaxMyopic.
        This Strategy class uses the rough_outcome heuristic to determine
        the best move for a player to choose.

    Instance Variables:
        max_depth: int        -- The number of game_states the minimax
                                algorithm will traverse in the game_state
                                tree before using the heuristic.

    Methods:
        - suggest_move: return a move that leads to the best
            predicted outcome.

    '''

    def __init__(self, interactive=False, max_depth=4):
        ''' (StrategyMinimaxMyopic, bool, int) -> NoneType

        Initialises (self) with all instance variables from Strategy,
        (interactive) capabilities and the maximum tree traversal depth of (d)

        Prerequisite: max_depth > 0

        >>> strategy = StrategyMinimaxMyopic(False, 10)
        >>> strategy.max_depth
        10
        '''

        Strategy.__init__(self, interactive)
        self.max_depth = max_depth

    def __eq__(self, other):
        ''' (StrategyMinimaxMyopic, object) -> bool

        Return True iff (other) is of the same instance as (self) and both
        (self) and (other) have the same max_depth.

        >>> strategy = StrategyMinimaxMyopic(False, 5)
        >>> better_strategy = StrategyMinimaxMyopic(False, 10)
        >>> strategy == strategy
        True
        >>> better_strategy == strategy
        False
        >>> better_strategy == 1.0
        False
        '''

        return isinstance(other, StrategyMinimaxMyopic) and (
            self.max_depth == other.max_depth)

    def __repr__(self):
        ''' (StrategyMinimaxMyopic) -> str

        Return a python interpretable string representing (self).

        >>> repr(StrategyMinimaxMyopic())
        'StrategyMinimaxMyopic(4)'
        '''

        return 'StrategyMinimaxMyopic({})'.format(self.max_depth)

    def __str__(self):
        ''' (StrategyMinimaxMyopic) -> str

        Return a human interpretable string representing (self).

        >>> str(StrategyMinimaxMyopic())
        'Myopic Minimax Strategy Class'
        '''

        return 'Myopic Minimax Strategy Class'

    def suggest_move(self, game_state, depth=0):
        r''' (StrategyMinimaxMyopic, GameState, int) -> Move

        (self) return a move that allows game_state.next_player to choose
        the most beneficial move. The (depth) parameter keeps track of the
        recursion depth.

        Overrides Strategy.suggest_move

        >>> from subtract_square_state import SubtractSquareState
        >>> game_state = SubtractSquareState('p1', False, 8)
        >>> game_strategy = StrategyMinimaxMyopic(False, 5)
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

            # check the current recursion depth for myopic, if not deep
            # enough continue as normal, else use heuristics.
            if depth <= self.max_depth:
                # get the minimax of the opponent's final score in children
                scores_list = [-1 * self.suggest_move(
                    child, depth + 1) for child in children]
                score = max(scores_list)
            else:
                score = game_state.rough_outcome()

            if depth == 0:
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
