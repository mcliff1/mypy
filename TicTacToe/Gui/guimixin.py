"""
a 'mixin' class for other frames

common methods for canned dialogs, spawning programs,
   simple text viewsers, PublicSubnetCidrBlock2

  this class must be mixed with a Frame (or a subclass) for its quit method
"""

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from launcher import PortableLauncher, System

class GuiMixin():
    def infobox(self, title, text, *args):
        return showinfo(title, text)


    def errorbox(self, text):
        showerror('Error!', text)

    def question(self, title, text, *args):
        return askyesno(title, text)  # return True/False



    def quit(self):
        ans = self.question('Verify quit', 'Are you sure you want to quit?')
        if ans:
            Frame.quit(self)

    def help(self):
        # FIXME:
        self.infobox('RTFM', 'See figure 1...')




    def clone(self, args=()):
        new = Toplevel()  # make new in-process version of me
        myclass = self.__class__   # instance's (lowest) class object
        myclass(new, *args)

    def spawn(self, pycmdline, wait=False):
        if not wait:
            PortableLauncher(pycmdline, pycmdline)()
        else:
            System(pycmdline, pycmdline)()







if __name__ == '__main__':
    class TestMixin(GuiMixin, Frame):
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack()
            Button(self, text='quit', command=self.quit).pack(fill=X)
            Button(self, text='help', command=self.help).pack(fill=X)
            Button(self, text='clone', command=self.clone).pack(fill=X)
            Button(self, text='spawn', command=self.other).pack(fill=X)

        def other(self):
            self.spawn('Gui/guimixin.py')  # spawn as a separat process

    TestMixin().mainloop()
