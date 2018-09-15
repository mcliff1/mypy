#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import random
import sys
import time
import itertools

from tkinter import *
from tkinter.messagebox import showinfo, askyesno
from gui.guimaker import GuiMakerWindowMenu
#from tkMessageBox import showinfo, askyesno
#import gui.guimaker

USER, MACHINE = 'user', 'machine'
X, O, EMPTY = 'X', 'O', ' '
FONT_SIZE = 50
DEGREE = 3
# MODE = 'Expert2'
# MODE = 'Random'
MODE = 'Smart'

DEBUG = 1

def traceif(*args):
    if DEBUG:
        trace(args)
        # apply(trace, args)

def trace(*args):
    for arg in args: print(arg,)
    print()

def pp(board):
    if DEBUG:
        rows = map((lambda row: '\n\t' + str(row)), board)
        # return string.join(rows)
        return ''.join(rows)


HELP_TEXT = """
PyToe 2.0
Sept, 2018
port to python3

PyToe 1.0
July, 1999
A Tic-tac-toe board game
written in Python with Tk
Programming Python 2E\n
Click in cells to move.
Command-line arguments:\n
-degree N sets board size
 N=number rows/columns\n
-mode M sets machine skill
 M=Minimax, Expert1|2,...\n
-fg F, -bg B
 F,B=color name\n
-fontsz N
 N=marks size\n
-goesFirst user|machine
-userMark X|O"""



########################################
# Base Class

class Record:
    def __init__(self):
        self.win = 0
        self.loss = 0
        self.draw = 0


class Board:
    """
    object represents the board with X, O markers
    """
    # POSITION_TOP_L = (0, 0)
    # POSITION_TOP_M = (1, 0)
    # POSITION_TOP_R = (2, 0)
    # POSITION_MID_L = (0, 1)
    # POSITION_MID_M = (1, 1)
    # POSITION_MID_R = (2, 1)
    # POSITION_BOT_L = (0, 2)
    # POSITION_BOT_M = (1, 2)
    # POSITION_BOT_R = (2, 2)


    def __init__(self, size=3):
        self.board = []
        self.size = size
        # how do I make this more pythonic?
        for col in range(size):
            self.board.append([0] * size)
        self.clear()

    def clear(self):
        """
        clears the board
        """
        for col in range(self.size):
            for row in range(self.size):
                self.board[col][row] = EMPTY


    def place_marker(self, position, marker):
        """
        position is tuple of (col, row)

        return True if move is possible, False if not
           either position is taken or invalid range
        """
        (col, row) = position
        if not col in range(self.size) \
           or not row in range(self.size):
            # index out of range
            return False

        if self.board[col][row] == EMPTY:
            self.board[col][row] = marker
            return True

        # else position is taken
        return False

    def is_win(self, marker):
        """
        returns true if the provider marker is
        in a victory condition (across, down or diagonal)
        """
        # check across
        for row in self.board:
            if row.count(marker) == self.size:
                return True

        for ndx in range(self.size):
            # check to see if everything in this column matches mark
            if all(map(lambda col: self.board[col][ndx] == marker, range(self.size))):
                return True

        # check diagonals 0,0 1,1 2,2 :   col = row
        if all(map(lambda ndx: self.board[ndx][ndx] == marker, range(self.size))):
            return True

        # check diagonals 0,2  1,1  2,0 :  col + row = (size-1)  [or row = (size-1) - col]
        if all(map(lambda ndx: self.board[ndx][(self.size - 1) - ndx] == marker, range(self.size))):
            return True

        return False

    def open_position(self):
        """
        return True if there is an open position

        if not Board.open_position():
            # this is a tie
            # (assuming no winner has been detected)

        to be a draw, there must be no available
        AFTER the win and loss checks occur
        """
        for row in self.board:
            if EMPTY in row:
                return True
        return False



    def __str__(self):
        rows = map((lambda row: '\n\t' + str(row)), self.board)
        # return string.join(rows)
        return ''.join(rows)


    def __repr__(self):
        return str(self.board)




class TicTacToeBase(GuiMakerWindowMenu):
    def __init__(self, parent=None, fg='black', bg='white',
                 font_size=FONT_SIZE, goes_first=USER, user_mark=X,
                 degree=DEGREE):
        self.next_move = goes_first
        self.user_mark = user_mark
        self.machine_mark = O if user_mark == X else X
        self.degree = degree
        self.record = Record()
        self.make_widgets = (lambda s=self, f=fg, b=bg, fs=font_size: s.draw_board(f, b, fs))

        GuiMakerWindowMenu.__init__(self, parent=parent)
        self.master.title('PyToe 2.0') #ported to python3
        if goes_first == MACHINE:
            self.machine_move() # else wait for a click

    def start(self):
        """
        on start up
        """
        self.help_button = None
        self.tool_bar = None
        self.menu_bar = [
            ('File', 0, [('Stats', 0, self.on_stats),
                         ('Quit', 0, self.quit)]),
            ('Help', 0, [('About', 0, self.on_about)])
        ]

    def draw_board(self, fg, bg, font_sz):
        """
        draws the game board
        """
        self.coord = {}
        self.label = {}
        self.board = []
        for i in range(self.degree):
            self.board.append([0] * self.degree)
            frm = Frame(self)
            frm.pack(expand=YES, fill=BOTH)
            for j in range(self.degree):
                widget = Label(frm, fg=fg, bg=bg,
                               text=' ', font=('courier', font_sz, 'bold'),
                               relief=SUNKEN, bd=4, padx=10, pady=10)
                widget.pack(side=LEFT, expand=YES, fill=BOTH)
                widget.bind('<Button-1>', self.on_left_click)
                self.coord[widget] = (i, j)
                self.label[(i, j)] = widget
                self.board[i][j] = EMPTY

    def on_left_click(self, event):
        """
        marks the users turn
        """
        label = event.widget
        row, col = self.coord[label]
        if self.next_move == USER and self.board[row][col] == EMPTY:
            label.config(text=self.user_mark)
            self.board[row][col] = self.user_mark
            self.next_move = MACHINE
            self.check_finish()
            self.machine_move()

    def machine_move(self):
        row, col = self.pick_move()
        self.board[row][col] = self.machine_mark
        label = self.label[(row, col)]
        label.config(text=self.machine_mark)
        self.check_finish()
        self.next_move = USER

    def clear_board(self):
        """resets all board location to EMPTY
        """
        for row, col in self.label.keys():
            self.label[(row,col)].config(text=' ')
            self.board[row][col] = EMPTY

    def check_draw(self, board=None):
        """
        loops through the board, if any row
        contains EMPTY then return false

        to be a draw, there must be no available
        AFTER the win and loss checks occur
        """
        board = board or self.board
        for row in board:
            if EMPTY in row:
                return False
        return True # EMPTY not in the grid -> draw


    def check_win(self, mark, board=None):
        """
        checks for win condition for the given marker
        """
        board = board or self.board
        for row in board:
            if row.count(mark) == self.degree:
                return True
        for ndx in range(self.degree):
            # check to see if everything in this column matches mark
            if all(map(lambda i: board[i][ndx] == mark, range(self.degree))):
                return True

        # check diagonals 0,0 1,1 2,2
        if all(map(lambda ndx: board[ndx][ndx] == mark, range(self.degree))):
            return True

        # check diagonals 0,2  1,1  2,0
        if all(map(lambda ndx: board[ndx][(self.degree - 1) - ndx] == mark, range(self.degree))):
            return True

    def check_finish(self):
        outcome = None
        if self.check_win(self.user_mark):
            outcome = 'You have won!'
            self.record.win = self.record.win + 1
        elif self.check_win(self.machine_mark):
            outcome = 'you lost'
            self.record.loss = self.record.loss + 1
        elif self.check_draw():
            outcome = 'it is a tie'
            self.record.draw = self.record.draw + 1

        if outcome:
            result = 'Game Over: ' + outcome
            if not askyesno('PyToe', result + '\n\nPlay again?'):
                self.on_stats()
                self.quit()
                sys.exit()
            else:
                self.clear_board()


    def on_about(self):
        showinfo('PyToe 2.0', HELP_TEXT)

    def on_stats(self):
        showinfo('PyToe Stats',
                 'Your results:\n'
                 'wins: %(win)d,  losses: %(loss)d,  draws: %(draw)d'
                 % self.record.__dict__)


    def __repr__(self):
        return pp(self.board)
        # return 'base tic tac toe'


########################################
#  Subclass definitions

class TicTacToeRandom(TicTacToeBase):
    """
    picks an empty slot at random
    """
    def pick_move(self):
        empties = []
        for row in range(self.degree):
            for col in range(self.degree):
                if self.board[row][col] == EMPTY:
                    empties.append((row, col))
        return random.choice(empties)


class TicTacToeSmart(TicTacToeBase):
    """
    pick imminent win or loss, else static score
    """
    # def __repr__(self):
    #     return 'here i am too'


    def pick_move(self):
        self.update()
        # time.sleep(1) # too fast!

        for row, col in itertools.product(range(self.degree), range(self.degree)):
            move = (row, col)
            if self.board[row][col] == EMPTY:
                if self._is_win(move):
                    return move

        for row, col in itertools.product(range(self.degree), range(self.degree)):
            move = (row, col)
            if self.board[row][col] == EMPTY:
                if self._is_block(move):
                    return move

        # let's score them
        #   try to adjust scoring,  if player moves first
        #     and picks bottom Right corner, computer will pick top left
        #      player then picks center and can win the game.
        best = 0
        # this is a representation of the board counts
        count_marks = self._count_across_down(), self._count_diagonal()
        # trace(count_marks)
        for row, col in itertools.product(range(self.degree), range(self.degree)):
            move = (row, col)
            if self.board[row][col] == EMPTY:
                score = self._score_move(move, count_marks)
                # trace(score)
                if score > best:
                    pick = move
                    best = score
        trace('Picked', pick, 'score', best)
        return pick

    def _count_across_down(self):
        """
        for each row, col count the number of marks (for each player)
        """
        count_rows = {}
        count_cols = {}
        for row, col in itertools.product(range(self.degree), range(self.degree)):
            mark = self.board[row][col]
            try:
                count_rows[(row, mark)] = count_rows[(row, mark)] + 1
            except KeyError:
                count_rows[(row, mark)] = 1
            try:
                count_cols[(col, mark)] = count_cols[(col, mark)] + 1
            except KeyError:
                count_cols[(col, mark)] = 1
        return count_rows, count_cols

    def _count_diagonal(self):
        """
        provides counts of the diagonal for each mark(player)
        """
        tally = {X: 0, O: 0, EMPTY: 0}
        count_diag1 = count_diag2 = tally.copy()
        for ndx in range(self.degree):
            # diag1 (0,0) (1,1) (2,2)
            mark = self.board[ndx][ndx]
            count_diag1[mark] = count_diag1[mark] + 1

            # diag2 (0,2) (1,1) (2,0)
            mark = self.board[ndx][(self.degree - 1) - ndx]
            count_diag2[mark] = count_diag2[mark] + 1
        return count_diag1, count_diag2

    def _is_win(self, move):
        """
        sets the piece on a copy of the board to check for win
        """
        (row, col) = move
        #board = self.board.copy()
        self.board[row][col] = self.machine_mark
        # trace(self.board)
        is_win = self.check_win(self.machine_mark)
        self.board[row][col] = EMPTY
        # trace(self.board)
        return is_win

    def _is_block(self, move):
        """
        checks to see if we would lose if the player went there
        """
        (row, col) = move
        #board = self.board
        self.board[row][col] = self.user_mark
        is_loss = self.check_win(self.user_mark)
        self.board[row][col] = EMPTY
        return is_loss


    def _score_move(self, move, count_marks):
        """
        col score is looking at all the 'X', 'O' and EMPTY
        (assume 'computer is X')
        11 * how many X's + 10 * how many O's + 9 * how many opens
        """
        (row, col) = move
        ((count_rows, count_cols), (count_diag1, count_diag2)) = count_marks
        return (
            count_cols.get((col, self.machine_mark), 0) * 11 +
            count_rows.get((row, self.machine_mark), 0) * 11 +
            count_diag1[self.machine_mark] * 11 +
            count_diag2[self.machine_mark] * 11
            +
            count_cols.get((col, self.user_mark), 0) * 10 +
            count_rows.get((row, self.user_mark), 0) * 10 +
            count_diag1[self.user_mark] * 10 +
            count_diag2[self.user_mark] * 10
            +
            count_cols.get((col, EMPTY), 0) * 11 +
            count_rows.get((row, EMPTY), 0) * 11 +
            count_diag1[EMPTY] * 11 +
            count_diag2[EMPTY] * 11
        )

########################################
#  Subclass definitions


def TicTacToe(mode=MODE, **args):
    """
    game object generator - external interface
    """
    try:
        classname = 'TicTacToe' + mode
        classobj = eval(classname)
    except Exception as e:
        print('Bad -mode flag, value:', mode)
    #return apply(eval(classname), (), args)
    #eval(classname, args)
    return globals()[classname](args)


#
# Command Line Logic
#


if __name__ == '__main__':
    if len(sys.argv) == 1:
        TicTacToe().mainloop()
    else:
        if len(sys.argv) == 1:
            TicTacToe().mainloop()
        else:
            needEval = ['-degree']
            args = sys.argv[1:]
            opts = {}
            # parse the opts and args two at a time
            for i in range(0, len(args), +2):
                if args[i] in needEval:
                    opts[args[i][1:]] = eval(args[i+1])
                else:
                    opts[args[i][1:]] = args[i+1]
                trace(opts)
                #apply(TicTacToe, (), opts).mainloop()
                TicTacToe(opts.get('mode', MODE)).mainloop()
