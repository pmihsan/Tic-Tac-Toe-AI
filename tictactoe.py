import sys 
import copy
import pygame
import random
import numpy as np

# CONSTANTS
# SHAPE & SIZE
WIDTH = 400
HEIGHT = 400

ROWS = 3
COLS = 3
SQSIZE = WIDTH // ROWS

LINE_WIDTH = 12
CIRCLE_WIDTH = 12
CROSS_WIDTH = 14

RADIUS = SQSIZE // 4

OFFSET = 40

# COLORS
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BG_COLOR)
pygame.display.set_caption("TIC TAC TOE AI")

mode = None

class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        # player 1 won - returns 1
        # player 2 won - returns 2
        # match draw - returns 0

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    initial_pos = (col * SQSIZE + SQSIZE // 2, 20)
                    final_pos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    ch = 'X' if self.squares[0][col] == 1 else 'O'
                    pygame.display.set_caption(f"TIC TAC TOE AI => Player {ch} won")
                    pygame.draw.line(screen, color, initial_pos, final_pos, LINE_WIDTH)
                
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    initial_pos = (20, row * SQSIZE + SQSIZE // 2)
                    final_pos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    ch = 'X' if self.squares[row][0] == 1 else 'O'
                    pygame.display.set_caption(f"TIC TAC TOE AI => Player {ch} won")
                    pygame.draw.line(screen, color, initial_pos, final_pos, LINE_WIDTH)

                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[0][0] == 2 else CROSS_COLOR
                initial_pos = (20, 20)
                final_pos = (WIDTH - 20, HEIGHT - 20)
                ch = 'X' if self.squares[0][0] == 1 else 'O'
                pygame.display.set_caption(f"TIC TAC TOE AI => Player {ch} won")
                pygame.draw.line(screen, color, initial_pos, final_pos, CROSS_WIDTH)

            return self.squares[0][0]

        # asc diagonal
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[0][2] == 2 else CROSS_COLOR
                initial_pos = (20, HEIGHT - 20)
                final_pos = (WIDTH - 20, 20)
                ch = 'X' if self.squares[0][2] == 1 else 'O'
                pygame.display.set_caption(f"TIC TAC TOE AI => Player {ch} won")
                pygame.draw.line(screen, color, initial_pos, final_pos, CROSS_WIDTH)

            return self.squares[0][2]

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        index = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[index] # (row, col)

    def minimax(self, board, maximizing):
        # terminal case
        result = board.final_state()

        # player 1 wins
        if result == 1:
            return 1, None # eval, move

        # player 2 wins
        if result == 2:
            return -1, None # eval, move

        # match draw 
        elif board.isfull():
            return 0, None # eval, move

        if maximizing: # maximizing player
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing: # minimizing player(ai)
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random ai
            eval = 'random'
            move = self.rnd(main_board)

        else:
            # mini max ai
            eval , move = self.minimax(main_board, False)
        
        print(f'AI has chosen: {move} with an eval of: {eval}')

        return move # row, col

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai' # or 'ai'
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        # background
        screen.fill(BG_COLOR)

        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw 'X' 
            # desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # draw 'O' 
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1
        ch = 'X' if self.player == 1 else 'O'
        pygame.display.set_caption(f"TIC TAC TOE AI => Player {ch}")

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
        mode = self.gamemode

    def isOver(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()


    def reset(self):
        self.__init__()

def main():

    # game object
    game = Game()
    mode = game.gamemode
    board = game.board
    ai = game.ai
    
    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # g - game mode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r - restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0 - random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1 - minimax ai
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                if game.isOver():
                    print("Match Finished")
                    if board.isfull():
                        pygame.display.set_caption(f"TIC TAC TOE AI => Match Draw(Press r to restart)")
                    game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)

            game.make_move(row, col)

            if game.isOver():
                    print("Match Finished")
                    if board.isfull():
                        pygame.display.set_caption(f"TIC TAC TOE AI => Match Draw(Press r to restart)")
                    game.running = False

        pygame.display.update()

main()