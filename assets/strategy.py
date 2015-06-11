class Strategy:
    '''Interface to suggest moves for a GameState.

    Must be subclassed to a concrete strategy.
    '''

    def __init__(self):
        '''(Strategy, bool) -> NoneType

        Create new Strategy (self).
        '''
        pass

    def suggest_move(self, state):
        '''(Strategy, GameState) -> Move

        Suggest a next move for state.
        '''
        raise NotImplementedError('Implement in a subclass')
