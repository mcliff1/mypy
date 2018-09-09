#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import random, sys, time
from Tkinter import *
#from tkMessageBox import showinfo, askyesno

User, Machine = 'user', 'machine'
X, O, Empty = 'X', 'O', ' '
Fontsz = 50
Degree = 3
Mode = 'Expert2'

Debug = 1

def traceif(*args):
    if Debug:
        apply(trace, args)

def trace(*args):
    for arg in args: print(arg,)
    print()

def pp(board):
    if Debug:
        rows = map((lambda row: '\n\t' + str(row)), board)
        return string.join(rows)






def TicTacToe(mode=Mode, **args):
    """
    game object generator - external interface
    """
    try:
        classname = 'TicTacToe' + mode
        classobj = eval(classname)
    except:
        print('Bad -mode flag, value:', mode)
    return apply(eval(classname), (), args)


#
# Command Line Logic
#
if __name__ == '__main__':
    if len(sys.argv) == 1:
        TicTacToe().mainloop()
    else:
        if (len.sys.argv) == 1:
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
                apply(TicTacToe, (), opts).mainloop()
