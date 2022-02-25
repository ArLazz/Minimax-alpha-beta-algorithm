import time


class game:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.current_state = [['.', '.', '.', '.'],
                              ['.', '.', '.', '.'],
                              ['.', '.', '.', '.'],
                              ['.', '.', '.', '.']]

        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        for i in range(0, 4):
            for j in range(0, 4):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > 3 or py < 0 or py > 3:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        # Vertical win
        for i in range(0, 4):
            if (self.current_state[0][i] != '.' and
                    self.current_state[0][i] == self.current_state[1][i] ==
                    self.current_state[2][i] == self.current_state[3][i]):
                return self.current_state[0][i]

        # Horizontal win
        for i in range(0, 4):
            if self.current_state[i] == ['X', 'X', 'X', 'X']:
                return 'X'
            elif self.current_state[i] == ['O', 'O', 'O', 'O']:
                return 'O'

        # Main diagonal win
        if (self.current_state[0][0] != '.' and
                self.current_state[0][0] == self.current_state[1][1] ==
                self.current_state[2][2] == self.current_state[3][3]):
            return self.current_state[0][0]

        # Second diagonal win
        if (self.current_state[0][3] != '.' and
                self.current_state[0][3] == self.current_state[1][2] ==
                self.current_state[2][1] == self.current_state[3][0]):
            return self.current_state[0][3]

        # Is whole board full?
        for i in range(0, 4):
            for j in range(0, 4):
            # There's an empty field, we continue the game
                if self.current_state[i][j] == '.':
                    return None

        # It's a tie!
        return '.'



    def max(self, alpha, beta, deep):
        maxv = -3
        px = None
        py = None
        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0, deep - 1)
        elif result == 'O':
            return (1, 0, 0, deep - 1)
        elif result == '.':
            return (0, 0, 0, deep - 1)
        if deep == 0:
            return (0,0,0,0)

        for i in range(0, 4):
            for j in range(0, 4):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j, min_d) = self.min(alpha, beta, deep)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if maxv >= beta:
                        return (maxv, px, py, deep - 1)

                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py, deep - 1)

    def min(self, alpha, beta, deep):
        minv = 3

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0, deep - 1)
        elif result == 'O':
            return (1, 0, 0, deep - 1)
        elif result == '.':
            return (0, 0, 0, deep - 1)
        if deep == 0:
            return (0,0,0,0)

        for i in range(0, 4):
            for j in range(0, 4):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j, max_d) = self.max(alpha, beta, deep)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

                    if minv <= alpha:
                        return (minv, qx, qy, deep - 1)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy, deep - 1)

    def play(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("It's a tie!")

                self.initialize_game()
                return

            if self.player_turn == 'X':

                while True:
                    start = time.time()
                    (m, qx, qy) = self.min(-3, 3, 1)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                    px = int(input('Insert the X coordinate: '))
                    py = int(input('Insert the Y coordinate: '))

                    qx = px
                    qy = py

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            else:
                (m, px, py) = self.max(-3, 3, 1)
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'


def main():
    g = game()
    g.play()


if __name__ == "__main__":
    main()
