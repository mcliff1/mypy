"""
p264 Programming Python v4
# FIXME: add better docs
"""
import sys
import os

pyfile = (sys.platform[:3] == 'win' and 'python.exe') or 'python'
pypath = sys.executable

IS_WINDOWS = sys.platform[:3].lower() == 'win'

def _fix_windows_path(cmdline):
    """
    change all / to \
    """
    split_line = cmdline.lstrip().split(' ') # split on spaces
    fixed_path = os.path.normpath(split_line[0]) # fix slashes
    return ' '.join([fixed_path] + split_line[1:]) # put back together

class LaunchMode():
    """
    on call to instance, annouce label and run Command
    subclasses format command lines as required in run()

    command should begin with name of script and not python
    """
    def __init__(self, label, command):
        self.what = label
        self.where = command

    def __call__(self):
        self.announce(self.what)
        self.run(self.where)

    def announce(self, text):
        print(text)

    def run(self, cmdline):   # subclasses must define run()
        assert False, 'run must be defined'



class System(LaunchMode):
    """
    run python scriupt named in shell from command line
    caveat: may block caller
    """
    def run(self, cmdline):
        cmdline = _fix_windows_path(cmdline)
        os.system('{} {}'.format(pypath, cmdline))

class Fork(LaunchMode):
    """
    run script in explicitly created new process
    """
    def run(self, cmdline):
        assert hasattr(os, 'fork')
        cmdline = cmdline.split()
        if os.fork() == 0:  # start new child proess
            os.execvp(pypath, [pyfile] + cmdline)  # run prog in new proc

class Spawn(LaunchMode):
    """
    run script in new process indepdent of caller
    """
    def run(self, cmdline):
        os.spawnv(os.P_DETACH, pypath, (pyfile, cmdline))



#
# best launcher for this platform
#
if IS_WINDOWS:
    PortableLauncher = Spawn
else:
    PortableLauncher = Fork

class QuietPortableLauncher(PortableLauncher):
    def announce(self, text):
        pass



def _selftest():
    """
    invoked by main
    """
    file = 'Gui/widgets.py'
    input('default mode...<press any key>...')
    launcher = PortableLauncher(file, file)
    launcher()


    if IS_WINDOWS:
        input('win start mode...<press any key>...')

if __name__ == '__main__':
    _selftest()
