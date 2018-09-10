"""
An extended Frame that makes windows and toolbards automatically

from Programming Python v4
O'Reilly publisher
author: Mark Lutz

(for python3)
"""
import sys
from tkinter import *
from tkinter.messagebox import showinfo

class GuiMaker(Frame):
    menuBar = []
    toolBar = []

    def __init__(self, parent=None):
        Frame.__init__(self, parent)


# Self test
if __name__ == '__main__':
    from guimixin import GuiMixin

    menuBar = [
        ('File', 0,
            [('Open', 0, lambda:0),
             ('Quit', 0, sys.exit)],
         'Edit', 0,
            [('Cut', 0, lambda:0),
             ('Paste', 0, lambda:0)]
        )
    ]
