#!/usr/local/bin/python
# -*- coding: utf-8 -*-

def TicTacToe(mode=Mode, **args):
    """
    Game Object Generator Class - external Interface
    """
    try:
        classname = 'TicTacToe' + mode
        classobj = eval(classname)
    except:
        print('Bad -mode flag value:', mode)
    return apply(eval(classname), (), args)

if __name__ == '__main__':
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
