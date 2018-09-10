"""
wraps up widget construction
"""
from tkinter import *

def frame(root, side=TOP, **extras):
    """
    constructs a frame
    """
    widget = Frame(root)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget


def label(root, side, text, **extras):
    """
    puts a label on the frame
    """
    widget = Label(root, text=text, relief=RIDGE)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget


def button(root, side, text, command, **extras):
    """
    puts a button on the frame
    """
    widget = Button(root, text=text, command=command)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget


def entry(root, side, linkvar, **extras):
    """
    An Entry for the frame
    """
    widget = Entry(root, relief=SUNKEN, textvariable=linkvar)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget


# test method
if __name__ == '__main__':
    app = Tk()
    frm = frame(app, TOP)
    label(frm, LEFT, 'SPAM')
    button(frm, BOTTOM, 'Press', lambda: print('Pushed'))
    mainloop()
