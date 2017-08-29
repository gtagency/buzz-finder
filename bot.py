from random import choice
PLAYER1 = 1
PLAYER2 = 2
DRAW = 3

class Game:
    def __init__(self, first, second):
        self.state = [[0 for _ in range(3)] for _ in range(3)]
        self.player1 = first
        self.player2 = second
        self.current = PLAYER1
        self.done = False

    def get_state(self):
        return self.state
    
    def check_win(self):

        for row in self.state:
            if row[0] == row[1] == row[2]:
                return row[0]

        transposed = list(zip(*self.state))
        for col in transposed:
            if col[0] == col[1] == col[2]:
                return col[0]
        
        if ((self.state[0][0] == self.state[1][1] == self.state[2][2]) or 
                (self.state[0][2] == self.state[1][1] == self.state[2][0])):
            return self.state[1][1]

        if all([all([x != 0 for x in row]) for row in self.state]):
            return DRAW
        
    def move(self):
        if self.done:
            return self.state

        if self.current == PLAYER1:
            self.current = PLAYER2
            self.state = self.player1.next(self.state)
        else:
            self.current = PLAYER1
            self.state = self.player2.next(self.state)
        
        win = self.check_win()
        if win:
            self.done = True
            if win == PLAYER1:
                print("Player 1 wins")
            elif win == PLAYER2:
                print("Player 2 wins")
            elif win == DRAW:
                print("Draw")

        return self.state

    def reset(self):
        self.state = [[0 for _ in range(3)] for _ in range(3)]
        self.current = PLAYER1
        self.done = False


class Bot:
    def __init__(self, team):
        self.team = team

    def next(self, game_state):
        moves = []
        for r, row in enumerate(game_state):
            for c, i in enumerate(row):
                if i == 0:
                    moves.append((r, c))

        r, c = choice(moves) 
        game_state[r][c] = self.team
        return game_state


