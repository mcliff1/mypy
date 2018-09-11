#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import random, sys, time
from tkinter import *
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
        self.make_widgets = (lambda s=self, f=fg, b=bg, fs=font_size: s.drawBoard(f, b, fs))

        GuiMakerWindowMenu.__init__(self, parent=parent)


########################################
#  Subclass definitions

class TicTacToeRandom(TicTacToeBase):
    """
    picks an empty slot at random
    """
    def pick_move(self):
        empties = []
        for row in self.degree:
            for col in self.degree:
                if not self.board[row][col]:
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
