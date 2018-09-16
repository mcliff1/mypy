#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Tic Tac Toe OO game
"""
import logging
import random

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

MODE = None
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

    def has_open_position(self):
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


    def list_open_positions(self):
        """
        returns a list(generator) of coordinate tuples for the board
        locations that are open
        """
        # return_list = []
        # for row in range(self.size):
        #     for col in range(self.size):
        #         if self.board[row][col] == EMPTY:
        #             location = (row, col)
        #             return_list.append(location)
        # return return_list
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == EMPTY:
                    position = (row, col)
                    yield position


    def __str__(self):
        rows = map((lambda row: '\n\t' + str(row)), self.board)
        # return string.join(rows)
        return ''.join(rows)


    def __repr__(self):
        return str(self.board)



class Player():
    """
    represents a player

    made this a super class and sub with real person and various AI's
    """

    def __init__(self, marker):
        self.marker = marker

    def move(self, board):
        """
        return true if the move is made
         otherwise return false if unable to move
        """
        #return board.place_marker((0, 0), self.marker)
        open_moves = list(board.list_open_positions())
        if open_moves:
            move = random.choice(open_moves)
            return board.place_marker(move, self.marker)
        # else no open moves
        return False



    def __repr__(self):
        return 'Player({})'.format(self.marker)


class Game():
    """
    two players and a board

    """

    def __init__(self):
        """
        moved player array into play scope

        sets up board and winner
        maybe add history of winners/losers
        """
        self.board = Board()
        #self.player1 = player1
        #self.player2 = player2
        self.winner = None


    def play(self, player1, player2):
        """
        # FIXME: make players a list

        A player will always have a .move(board) method
        that will update the board and return True, otherwise
        if unable to update the board returns False

        this will run until either one of the players is
        declared a winner by the Board.is_win() method OR
        the Board.has_open_postion() method returns False

        at this thme the Game.winner attribute will be set
        to the winning player
        """
        while self.board.has_open_position():
            if not player1.move(self.board) or \
               self.board.is_win(player1.marker):
                break

            print(self.board)

            if not player2.move(self.board) or \
               self.board.is_win(player2.marker):
                break

            print(self.board)

            # for player in players:
            #     if not player.move(self.board) or \
            #         self.board.is_win(player.marker):
            #         break


        if self.board.is_win(player1.marker):
            self.winner = player1
        elif self.board.is_win(player2.marker):
            self.winner = player2
        else:
            # no open positions, and no winner, it's a draw
            self.winner = None

        # self.winner = None
        # for player in players:
        #     if self.board.is_win(player.marker)
        #         self.winner = player
        #         break


    def reset(self):
        self.board = Board()
        self.winner = None


def TicTacToe(mode=MODE, **args):
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
