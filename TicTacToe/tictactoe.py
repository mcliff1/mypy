#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Tic Tac Toe OO game
"""

X, O, EMPTY = 'X', 'O', ' '


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
