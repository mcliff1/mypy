#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Board object for Connect Four

Created 10/6/18
"""
import logging
import copy
import itertools


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class Board:
    """
    object represents the board with X, O markers
    """

    EMPTY = ' '
    """
    class level indicator of empty position
    """


    def __init__(self, board=None, size=8):
        """
        initializes a board

        if board is provided we use that and size is ignored
        """
        self.size = size
        # how do I make this more pythonic?
        if board:
            self.board = board.board.copy()
        else:
            self.board = []
            for _ in range(size):
                self.board.append([0] * size)
        self.clear()


    def clear(self):
        """
        clears the board
        """
        self.history = []
        # this will be a list of tuples 'mark', 'move', 'board' (at start)

        for col in range(self.size):
            for row in range(self.size):
                self.board[row][col] = Board.EMPTY

    def _col(self, col):
        return list(map(lambda ndx: self.board[ndx][col], range(self.size)))

    def place_marker(self, col, marker):
        """
        position is int of col

        return True if move is possible, False if not
           either position is taken or invalid range
        """
        if not col in range(self.size):
            # index out of range
            return False

        if Board.EMPTY not in self._col(col):
            print('# the column is full')
            return False

        # depth to go on the row
        row = len(list(filter(lambda x: x == Board.EMPTY, self._col(col)))) - 1
        print('using (col,row) ({},{})'.format(col, row))

        if self.board[row][col] == Board.EMPTY:
            # self.history.append((marker, (col, row), self.encode()))
            self.history.append((marker, col, copy.deepcopy(self.board)))
            self.board[row][col] = marker
            return True

        # else position is taken
        return False

    def is_win(self, marker, connect_win=4):
        """
        returns true if the provider marker is
        in a victory condition (across, down or diagonal)
        """
        # check across
        for row in self.board:
            if row.count(marker) == self.size:
                return True

        # check rows and columns in same loop
        for ndx, row in enumerate(self.board):
            # check across
            series = [row[ndx2:ndx2+connect_win] for ndx2 in range(self.size-connect_win)]
            for seq in series:
                if seq.count(marker) == connect_win:
                    return True

            # check the columns
            c = self._col(ndx)
            series = [c[ndx2:ndx2+connect_win] for ndx2 in range(self.size-connect_win)]
            for seq in series:
                if seq.count(marker) == connect_win:
                    return True



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
            if Board.EMPTY in row:
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
                if self.board[row][col] == Board.EMPTY:
                    position = (row, col)
                    yield position

    def count_across_down(self):
        """
        Used by scoring algorithms
        for each row, col count the number of marks (for each player)
        """
        count_rows = {}
        count_cols = {}
        for row, col in itertools.product(range(self.size), range(self.size)):
            mark = self.board[row][col]
            try:
                count_rows[(row, mark)] = count_rows[(row, mark)] + 1
            except KeyError:
                count_rows[(row, mark)] = 1
            try:
                count_cols[(col, mark)] = count_cols[(col, mark)] + 1
            except KeyError:
                count_cols[(col, mark)] = 1
        return count_rows, count_cols

    def _diagonals(self):
        """
        Gets list of all diagonal lists

        this is down and to the right
        """
        diagonals = []
        for ndx in range(self.size):
            diagonals.append([self.board[x][x+ndx] for x in range(self.size - ndx)])
            # otherwise we double count
            if ndx != 0:
                diagonals.append([self.board[x][x-ndx] for x in range(ndx, self.size)])

        return diagonals
        # row,column
        #(0,0)
        #(1,0) (0,1)
        #(2,0) (1,1) (0,2)
        #..
        #(7,0) (6,1) (5,2) .. (1,6) (0,7)
        #(7,1) (6,2) (5,3) .. (1,7)
        #(7,2) (6,3), (5,4) .. (2,7)
        # ..
        #(7,7)
        self.board[ndx-x][x] for x in  range(ndx+1)]  ndx 0..7
        self.board[(size-1+ndx)-x][x] for x in range(ndx, size)] ndx 1..7

    def count_diagonal(self):
        """
        Used by scoring algorithms
        provides counts of the diagonal for each mark(player)
        """
        # tally = { mark:X: 0, O: 0, EMPTY: 0}
        # count_diag1 = count_diag2 = tally.copy()
        count_diag1 = count_diag2 = {}
        for ndx in range(self.size):
            # diag1 (0,0) (1,1) (2,2)
            mark = self.board[ndx][ndx]
            count_diag1[mark] = count_diag1.get(mark, 0) + 1

            # diag2 (0,2) (1,1) (2,0)
            mark = self.board[ndx][(self.size - 1) - ndx]
            count_diag2[mark] = count_diag2.get(mark, 0) + 1
        return count_diag1, count_diag2

    def get_markers(self):
        """
        returns a list of the markers that are on the board
        at most it will be 2 element list, it could be 1 if only one player moved
        or 0 if the board is clear
        """
        marker_list = []
        for row, col in itertools.product(range(self.size), range(self.size)):
            if self.board[row][col] != Board.EMPTY and self.board[row][col] not in marker_list:
                marker_list.append(self.board[row][col])
            if len(marker_list) > 1:
                # there can be at most two differnt markers
                break
        return marker_list



    def __str__(self):
        rows = map((lambda row: '\n\t' + str(row)), self.board)
        # return string.join(rows)
        return ''.join(rows)


    def __repr__(self):
        return str(self.board)

    @staticmethod
    def encode(board_list, marker):
        """
        returns a int representation of the board that is encoded
        from the persepective of the marker specified, it is expected to be
        the winner players, and store the board configurations from the persepective
        of the winning player to make predictions

        Draws are ??? ignored for now, since I would need to pick a marker

        start by a (size)^2 digit base three number:
            empty = 0
            marker/winner = 1
            other = 2
        positions are (0,0), (0,1), ..., (0,n), (1,0), ..., (n,n)

        this should only be called after there is a winner
        """
        # xlation = {EMPTY: '0', X: '1', O: '2'}
        # since I am not keeping track of the marker other than winner use else
        base3_str = ''
        # for row in range(len(board_list)):
        #     for col in range(len(board_list)):
        #         #base3_str += xlation[self.board[row][col]]
        #         if board_list[row][col] == EMPTY:
        #             base3_str += '0'
        #         elif board_list[row][col] == marker:
        #             base3_str += '1'
        #         else: # expected to be the loser marker
        #             base3_str += '2'
        for row in board_list:
            for location in row:
                #base3_str += xlation[self.board[row][col]]
                if location == Board.EMPTY:
                    base3_str += '0'
                elif location == marker:
                    base3_str += '1'
                else: # expected to be the loser marker
                    base3_str += '2'
        # returns this string representation of base 3
        return int(base3_str, 3)



def main():
    """
    test method to run if called from main
    """
    board = Board()
    print(list(board.list_open_positions()))

    print(board)
    board.place_marker((0, 0), 'X')
    board.place_marker((0, 1), 'X')
    board.place_marker((0, 2), 'X')
    print(board)
    print(board.is_win('X'))
    print(list(board.list_open_positions()))
    print(board.history)

    board.clear()
    board.place_marker((0, 1), 'X')
    board.place_marker((0, 0), 'O')
    board.place_marker((0, 2), 'X')
    board.place_marker((1, 1), 'O')
    board.place_marker((1, 0), 'X')
    board.place_marker((2, 2), 'O')
    print(board)
    print(board.is_win('O'))
    print(list(board.list_open_positions()))


if __name__ == '__main__':
    main()
