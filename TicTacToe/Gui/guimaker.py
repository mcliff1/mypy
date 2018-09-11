"""
An extended Frame that makes windows and toolbards automatically

from Programming Python v4
O'Reilly publisher
author: Mark Lutz

(for python3)
"""
import sys
from tkinter import Frame, Menubutton, Menu, Button, Label
from tkinter import LEFT, RIGHT, TOP, BOTTOM, YES, BOTH
from tkinter import DISABLED, FLAT, RAISED, SUNKEN, X
from tkinter.messagebox import showinfo

class GuiMaker(Frame):
    """
    Main Gui Maker class
    """
    menu_bar = []
    tool_bar = []
    help_button = True

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.start()
        self._make_menu_bar()
        self._make_tool_bar()
        self._make_widgets()

    def _make_menu_bar(self):
        """
        make menu bar at the top (TK9.0 menus below)
        expand=no, fill=X so same width on resize
        """
        menu_bar = Frame(self, relief=RAISED, bd=2)
        menu_bar.pack(side=TOP, fill=X)

        for (name, key, items) in self.menu_bar:
            mbutton = Menubutton(menu_bar, text=name, underline=key)
            mbutton.pack(side=LEFT)
            pulldown = Menu(mbutton)
            self._add_menu_items(pulldown, items)
            mbutton.config(menu=pulldown)

        if self.help_button:
            Button(menu_bar, text='Help', cursor='gumby', relief=FLAT,
                   command=self.help).pack(side=RIGHT)


    def _add_menu_items(self, menu, items):
        for item in items:
            if item == 'separator':
                menu.add_separator({})
            elif isinstance(item, list):
                for num in item:
                    menu.entryconfig(num, state=DISABLED)
            elif not isinstance(item[2], list):
                menu.add_command(label=item[0], underline=item[1], command=item[2])
            else:
                pullover = Menu(menu)
                self._add_menu_items(pullover, item[2])
                menu.add_cascade(label=item[0], underline=item[1], menu=pullover)

    def _make_tool_bar(self):
        """
        makes mutton bar at bottom, if any
        expand=no, fill=x so same width on resize
        could support images too (woudl need prebuil gifs or PIL)
        """
        if self.tool_bar:
            tool_bar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
            tool_bar.pack(side=BOTTOM, fill=X)
            for (name, action, where) in self.tool_bar:
                Button(tool_bar, text=name, command=action).pack(where)

    def _make_widgets(self):
        """
        make 'middle' part last, so menu/toolbar always on top/bottom and clipped last

        override this default, pack middle any side
        for grid: grid middle part in a packed frame
        """
        name = Label(self, width=40, height=10,
                     relief=SUNKEN, bg='white',
                     text=self.__class__.__name__,
                     cursor='crosshair')
        name.pack(expand=YES, fill=BOTH, side=TOP)

    def help(self):
        """ override in subclass
        """
        showinfo('Help', 'Sorry, no help for ' + self.__class__.__name__)

    def start(self):
        """ override in subclass
        """
        pass


###########################################
# Customize for Tk8.0 main window instead of frame
GuiMakerFrameMenu = GuiMaker

class GuiMakerWindowMenu(GuiMaker):
    def make_menu_bar(self):
        menu_bar = Menu(self.master)
        self.master.config(menu=menu_bar)


###########################################
# Self test
if __name__ == '__main__':
    from guimixin import GuiMixin

    MENU_BAR = [
        ('File', 0,
         [('Open', 0, lambda: 0),
          ('Quit', 0, sys.exit)],
         'Edit', 0,
         [('Cut', 0, lambda: 0),
          ('Paste', 0, lambda: 0)]
        )
    ]

    TOOL_BAR = [('Quit', sys.exit, {'side': LEFT})]

    class TestAppFrameMenu(GuiMixin, GuiMakerFrameMenu):
        def start(self):
            self.menu_bar = MENU_BAR
            self.tool_bar = TOOL_BAR
