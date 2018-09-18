#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Tic Tac Toe OO game
"""
import logging
import random
import sys
import copy

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

MODE = None
#X, O, EMPTY = 'X', 'O', ' '
EMPTY = ' '


class Board:
    """
    object represents the board with X, O markers
    """

    def __init__(self, board=None, size=3):
        self.size = size
        # how do I make this more pythonic?
        if board:
            self.board = board
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
            # self.history.append((marker, (col, row), self.encode()))
            self.history.append((marker, (col, row), copy.deepcopy(self.board)))
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


    def encode(self, winner):
        """
        returns a int representation of the board that is encoded
        from the persepective of the marker specified, it is expected to be
        the winner players, and store the board configurations from the persepective
        of the winning player to make predictions

        Draws are ??? ignored for now, since I would need to pick a marker

        start by a (size)^2 digit base three number:
            empty = 0
            winner = 1
            other = 2
        positions are (0,0), (0,1), ..., (0,n), (1,0), ..., (n,n)

        this should only be called after there is a winner
        """
        # xlation = {EMPTY: '0', X: '1', O: '2'}
        # since I am not keeping track of the marker other than winner use else
        base3_str = ''
        for row in range(self.size):
            for col in range(self.size):
                #base3_str += xlation[self.board[row][col]]
                if self.board[row][col] == EMPTY:
                    base3_str += '0'
                elif self.board[row][col] == winner:
                    base3_str += '1'
                else: # expected to be the loser marker
                    base3_str += '2'
        # returns this string representation of base 3
        return int(base3_str, 3)




class Player():
    """
    represents a player

    made this a super class and sub with real person and various AI's
    """

    def __init__(self, name, marker):
        """
        it is expected to be either 'X' or 'O' for this game,
        as long as the two players have separate markers

        We have name so that we can use different implementations X or O
        """
        self.marker = marker
        self.name = name

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
        return 'Player({}-{})'.format(self.name, self.marker)


class PlayerSmart(Player):
    """
    represents a smart player
    """
    def move(self, board):
        #self.update()
        # time.sleep(1) # too fast!
        open_moves = list(board.list_open_positions())
        for move in open_moves:
            if self._is_win(move, board):
                return move

        for move in open_moves:
            if self._is_block(move):
                return move

        # let's score them
        #   try to adjust scoring,  if player moves first
        #     and picks bottom Right corner, computer will pick top left
        #      player then picks center and can win the game.
        best = 0
        # this is a representation of the board counts
        count_marks = self._count_across_down(), self._count_diagonal()
        # trace(count_marks)
        for move in open_moves:
            score = self._score_move(move, count_marks)
            # trace(score)
            if score > best:
                pick = move
                best = score
        return pick

    def _count_across_down(self):
        """
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

    def _count_diagonal(self):
        """
        provides counts of the diagonal for each mark(player)
        """
        tally = {X: 0, O: 0, EMPTY: 0}
        count_diag1 = count_diag2 = tally.copy()
        for ndx in range(self.degree):
            # diag1 (0,0) (1,1) (2,2)
            mark = self.board[ndx][ndx]
            count_diag1[mark] = count_diag1[mark] + 1

            # diag2 (0,2) (1,1) (2,0)
            mark = self.board[ndx][(self.degree - 1) - ndx]
            count_diag2[mark] = count_diag2[mark] + 1
        return count_diag1, count_diag2

    def _is_win(self, move):
        """
        sets the piece on a copy of the board to check for win
        """
        (row, col) = move
        #board = self.board.copy()
        self.board[row][col] = self.machine_mark
        # trace(self.board)
        is_win = self.check_win(self.machine_mark)
        self.board[row][col] = EMPTY
        # trace(self.board)
        return is_win

    def _is_block(self, move):
        """
        checks to see if we would lose if the player went there
        """
        (row, col) = move
        #board = self.board
        self.board[row][col] = self.user_mark
        is_loss = self.check_win(self.user_mark)
        self.board[row][col] = EMPTY
        return is_loss


    def _score_move(self, move, count_marks):
        """
        col score is looking at all the 'X', 'O' and EMPTY
        (assume 'computer is X')
        11 * how many X's + 10 * how many O's + 9 * how many opens
        """
        (row, col) = move
        ((count_rows, count_cols), (count_diag1, count_diag2)) = count_marks
        return (
            count_cols.get((col, self.machine_mark), 0) * 11 +
            count_rows.get((row, self.machine_mark), 0) * 11 +
            count_diag1[self.machine_mark] * 11 +
            count_diag2[self.machine_mark] * 11
            +
            count_cols.get((col, self.user_mark), 0) * 10 +
            count_rows.get((row, self.user_mark), 0) * 10 +
            count_diag1[self.user_mark] * 10 +
            count_diag2[self.user_mark] * 10
            +
            count_cols.get((col, EMPTY), 0) * 11 +
            count_rows.get((row, EMPTY), 0) * 11 +
            count_diag1[EMPTY] * 11 +
            count_diag2[EMPTY] * 11
        )

    def __repr__(self):
        return 'SmartPlayer({}-{})'.format(self.name, self.marker)



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



    def play(self, player1, player2, trace=True):
        """
        trace option to draw the screen after each move (otherwise no display)


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
        method = 'play():'
        if player1.marker == player2.marker:
            LOGGER.error('%sboth players can not have the same marker "%s"',
                         method, player1.marker)
            return

        while self.board.has_open_position():
            if not player1.move(self.board) or \
               self.board.is_win(player1.marker):
                break

            if trace:
                print(self.board)

            if not player2.move(self.board) or \
               self.board.is_win(player2.marker):
                break

            if trace:
                print(self.board)

            # for player in players:
            #     if not player.move(self.board) or \
            #         self.board.is_win(player.marker):
            #         break

        if trace and self.board.has_open_position():
            print(self.board)

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
        """
        resets the game (a new board and clears winner)
        """
        self.board = Board()
        self.winner = None


    def history(self):
        """
        returns the history of the game
        """
        return self.board.history





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
