"""
NAME
    strategy_minimax_memoize

DESCRIPTION
    This module contains the implementation of the minimax strategy
    used by the StrategyMinimaxOverkill class. Minimax is a strategy crucial
    to make a strong AI. Memoization is an optimization technique to
    make it faster.

FUNCTIONS
    minimax

CLASSES
    strategy.Strategy
        StrategyMinimaxOverkill
"""

import random
from strategy import Strategy


class StrategyMinimaxOverkill(Strategy):
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
    def __init__(self, interactive=False):
        ''' (StrategyMinimaxOverkill) -> NoneType

        Initialize new instance of StrategyMinimaxOverkill
        that inherits all properties of Strategy and has
        a memoization_dict with cached GameState results.

        '''
        # Extend Strategy
        Strategy.__init__(self, interactive)
        self.memoization_dict = {}

    def __eq__(self, other):
        ''' (StrategyMinimaxOverkill, object) -> bool

        Return True iff (other) is of the same instance as (self)

        >>> strategy = StrategyMinimaxOverkill()
        >>> better_strategy = StrategyMinimaxOverkill()
        >>> better_strategy == strategy
        True
        >>> better_strategy == 1.0
        False
        '''

        return isinstance(other, StrategyMinimaxOverkill)

    def __repr__(self):
        ''' (StrategyMinimaxOverkill) -> str

        Return a python interpretable string representing (self).

        >>> repr(StrategyMinimaxOverkill())
        'StrategyMinimax()'
        '''

        return 'StrategyMinimaxOverkill()'

    def __str__(self):
        ''' (StrategyMinimaxOverkill) -> str

        Return a human interpretable string representing (self).

        >>> str(StrategyMinimax())
        'Minimax Strategy Class'
        '''

        return 'Minimax Strategy Class'

    def suggest_move(self, game_state, root=True, p1_max=-1.0, p2_max=-1.0):
        r''' (StrategyMinimaxOverkill, GameState, bool, ) -> Move

        (self) return a move that lets game_state.next_player most likely to
        win current game_state.(root) parameter will return a move if set
        true or the bool represntaion of the best move if False.

        Overrides Strategy.suggest_move

        >>> from subtract_square_state import SubtractSquareState
        >>> game_state = SubtractSquareState('p1', False, 8)
        >>> game_strategy = StrategyMinimaxOverkill()
        >>> game_strategy.suggest_move(game_state).amount
        1
        '''
        if(game_state.__repr__() in self.memoization_dict):
            return self.memoization_dict[game_state.__repr__()]

        # get the available moves for current game_state
        available_moves = game_state.possible_next_moves()
        if available_moves:
            # make a list of the child game states
            children = [
                game_state.apply_move(move) for move in available_moves
            ]
            # get the minimax of the opponents final score in child game states
            # multiplying by -1 will give you the current player's score
            scores_list = []
            for i in range(len(children)):
                # Initialize variables local to for loop
                child = children[i]
                child_score = -1.0 * self.suggest_move(
                    child,
                    False,
                    p2_max,
                    p1_max)
                # Get max score for p1 and p2 (in current state)
                p1_max = max(child_score, p1_max)
                p2_max = -1.0 * max(child_score, p2_max)
                # If the move is not as good as the best
                # move that we have already found
                # ignore the branch
                if(p1_max > child_score):
                    if not root:
                        return child_score
                scores_list.append(child_score)
            score = max(scores_list)
            if root:
                # then we want to return a Move object with the highest score
                return_moves = [available_moves[i] for i in range(
                    len(available_moves)) if scores_list[i] == score]
                selected_move = random.choice(return_moves)
                self.memoization_dict[game_state.__repr__()] = selected_move
                return selected_move
            else:
                # we're still in the computing minimax, return the final
                # score of game_state
                self.memoization_dict[game_state.__repr__()] = score
                return score
        else:
            # there are no moves, hence the game has ended
            # return the next_players outcome of the game
            self.memoization_dict[game_state.__repr__()] = game_state.outcome()
            return game_state.outcome()
