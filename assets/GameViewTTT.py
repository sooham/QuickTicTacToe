import tkinter


class TTTClient:

    def __init__(self, gameview):
        # window settings
        self.window = tkinter.Tk()
        self.window.title("TickTacToe")

        # Widget instantiations
        self.button_reference = {}
        for x in range(3):
            for y in range(3):
                self.button_reference[(x, y)] = tkinter.Button(
                    self.window, text="", width=3, height=1,
                    command=lambda xcoord=x, ycoord=y: gameview.update(xcoord, ycoord)
                    )
                self.button_reference[(x, y)].grid(row=y, column=x)

        self.feedback_label = tkinter.Label(
            self.window, text="Select a spot", width=10, height=1, bg="white smoke",
            )
        self.feedback_label.grid(
            row=3, columnspan=3, sticky=tkinter.E+tkinter.W
            )


class GameViewTTT:
    '''
    A game view for a two-player, sequential move, zero-sum,
    perfect-information game.
    '''

    def __init__(self, client, state, strategy):
        '''(GameViewTTT, TTTClient.__class__,GameState.__class__,
            Strategy.__class__) -> NoneType

        Create TTTGameView self for game with state for client, where
        computer uses strategy.
        '''
        self.state = state('p1')    # human player
        self.strategy = strategy()
        self.client = client(self)
        self.client.window.mainloop()

    def update(self, x, y):
        ''' (GameViewTTT) -> NoneType

        Make all game logical moves after user button press.
        '''
        m = MoveTTT((x, y))

        if m not in self.state.possible_next_moves():
            # The move was illegal.
            self.client.feedback_label["text"] = "Illegal move"
            return

        # add move to the game state and update client
        self.state = self.state.apply_move(m)
        self.client.button_reference[(x, y)]["text"] = self.state.board[(x, y)]

        if self.state.possible_next_moves() == []:
            if self.state.winner('p2'):
                # p2, the computer, wins
                self.client.feedback_label["text"] = "You lost."
            elif self.state.winner('p1'):
                # p1, the human challenger, wins
                self.client.feedback_label["text"] = "You Won!"
            else:
                self.client.feedback_label["text"] = "You tied..."
            return

        # The computer makes a move.
        m = self.strategy.suggest_move(self.state)

        self.state = self.state.apply_move(m)
        self.client.button_reference[m.position]["text"] = self.state.board[m.position]

        if self.state.possible_next_moves() == []:
            if self.state.winner('p2'):
                # p2, the computer, wins
                self.client.feedback_label["text"] = "You lost."
            elif self.state.winner('p1'):
                # p1, the human challenger, wins
                self.client.feedback_label["text"] = "You Won!"
            else:
                self.client.feedback_label["text"] = "You tied..."

if __name__ == '__main__':
    from MoveTTT import MoveTTT
    from GameStateTTT import GameStateTTT
    from StrategyMinimax import StrategyMinimax

    TickTacToe = GameViewTTT(TTTClient, GameStateTTT, StrategyMinimax)
