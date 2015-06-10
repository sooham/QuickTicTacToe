"""
NAME
    strategy_minimax_prune

DESCRIPTION
    The implementation of the standard minimax algorithm optimised for
    efficient with pruning.

    The StrategyMinimaxPrune is subclassed from the generic Strategy algorithm.

CLASSES
    strategy.Strategy
        StrategyMinimaxPrune
"""
import random
from strategy import Strategy


class StrategyMinimaxPrune(Strategy):
    '''
        A faster implementation for minimax, called StrategyMinimaxPrune.
        This Strategy class uses pruning to determine the best move for
        a player to choose. Significant time is saved on gamestate
        generation and game-tree traversal.

    Methods:
        - suggest_move: return a move that leads to the best
            predicted outcome.
    '''
    # No need for __init__ as this class has no instance variables

    def __eq__(self, other):
        ''' (StrategyMinimaxPrune, object) -> bool

        Return True iff (other) is of the same instance as (self)

        >>> strategy = StrategyMinimaxPrune()
        >>> better_strategy = StrategyMinimaxPrune()
        >>> better_strategy == strategy
        True
        >>> better_strategy == 1.0
        False
        '''

        return isinstance(other, StrategyMinimaxPrune)

    def __repr__(self):
        ''' (StrategyMinimaxPrune) -> str

        Return a python interpretable string representing (self).

        >>> repr(StrategyMinimaxPrune())
        'StrategyMinimaxPrune()'
        '''

        return 'StrategyMinimaxPrune()'

    def __str__(self):
        ''' (StrategyMinimaxPrune) -> str

        Return a human interpretable string representing (self).

        >>> str(StrategyMinimaxPrune())
        'Prune Minimax Strategy Class'
        '''

        return 'Prune Minimax Strategy Class'

    def suggest_move(self, game_state, root=True):
        r''' (StrategyMinimaxPrune, GameState, bool) -> Move

        Return a Move that maximises the chance of game_state.next_player
        winning. The depth parameter will keep track of the recursion depth
        and return a Move if depth == 0. The upper and lower bounds are used
        for pruning purposes.

        Overrides Strategy.suggest_move

        # doctest here
        '''

        # get the available moves for current game_state
        available_moves = game_state.possible_next_moves()
        if available_moves:
            scores_list = [-2]
            children = [
                game_state.apply_move(move) for move in available_moves
            ]
            # get the minimax of the opponents final score in
            # child game states multiplying by -1 will give
            # the current player's score
            for child in children:
                game_score = -1 * self.suggest_move(child, False)
                # according to the depth of the search, compare with upper
                # and lower limits and prune.
                scores_list.append(game_score)
                if game_score <= max(scores_list):
                    if root:
                        return available_moves[
                            scores_list.index(max(scores_list))
                        ]
                    else:
                        return max(scores_list)

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
