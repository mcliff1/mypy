#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import random, sys, time
from tkinter import *
from tkinter.messagebox import showinfo, askyesno
from gui.guimaker import GuiMakerWindowMenu
#from tkMessageBox import showinfo, askyesno
#import gui.guimaker

USER, MACHINE = 'user', 'machine'
X, O, EMPTY = 'X', 'O', ' '
FONT_SIZE = 50
DEGREE = 3
#MODE = 'Expert2'
MODE = 'Random'

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
        ''.join(rows)


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


########################################
#  Subclass definitions


def TicTacToe(mode=MODE, **args):
    """
    game object generator - external interface
    """
    try:
        classname = 'TicTacToe' + mode
        classobj = eval(classname)
    except:
        print('Bad -mode flag, value:', mode)
    #return apply(eval(classname), (), args)
    eval(classname, args)


#
# Command Line Logic
#
if __name__ == '__main__':
    if len(sys.argv) == 1:
        # # FIXME: this should take the 'Random' part from MODE
        #TicTacToe().mainloop()
        TicTacToeRandom().mainloop()
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
                TicTacToe(opts).mainloop()
