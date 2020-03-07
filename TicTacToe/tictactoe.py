#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Tic Tac Toe OO game

Base Player class is in game module

"""
import logging
import random

from board import Board
from player import Player
from game import Series
# from .game import Game

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

MODE = None

class PlayerHuman(Player):
    """
    represents a human player
    """
    def __init__(self, marker):
        self.marker = marker

    def move(self, board):
        if not board.has_open_position():
            return False

        valid_move = False
        while not valid_move:
            print('human player select move:')
            choice = input()
            move = tuple(map(int, choice.split(',')))
            valid_move = board.place_marker(move, self.marker)
            if not valid_move:
                print('location {} already taken'.format(move))
        return True


class PlayerData(Player):
    """
    represents a player using the history
    """
    def __init__(self, marker, winning_moves):
        """
        winning moves is result of series of games
          (s.winning_moves)
        """
        self.marker = marker

        # list of list elem [(board_encoding, (mv_x,mv_y)), count]
        move_scores = [(x, winning_moves.count(x)) for x in set(winning_moves)]
        #_move_summary =

        board_set = {board_move[0] for  board_move in winning_moves}

        self._move_data = {}
        print('there are {} board_sets'.format(len(board_set)))
        for board in board_set:
            move_summary = {x[0][1]: x[1] for x in move_scores if x[0][0] == board}
            self._move_data[board] = max(move_summary, key=lambda k: move_summary[k])


    def move(self, board):
        # assume winning_moves is set

        #sublist of the moves for this board
        board_encoding = Board.encode(board.board, self.marker)
        data_driven_move = self._move_data.get(board_encoding)

        # if data provides no moves to score call the super method
        if not data_driven_move:
            return super().move(board)

        return board.place_marker(data_driven_move, self.marker)


class PlayerSmart(Player):
    """
    represents a smart player
    """
    def move(self, board):
        #self.update()
        # time.sleep(1) # too fast!
        open_moves = list(board.list_open_positions())
        if not open_moves:
            return False

        for move in open_moves:
            if self._is_win(move, board):
                return board.place_marker(move, self.marker)

        for move in open_moves:
            if self._is_block(move, board):
                return board.place_marker(move, self.marker)

        # let's score them
        #   try to adjust scoring,  if player moves first
        #     and picks bottom Right corner, computer will pick top left
        #      player then picks center and can win the game.
        best = 0
        # this is a representation of the board counts
        count_marks = board.count_across_down(), board.count_diagonal()
        # trace(count_marks)
        for move in open_moves:
            marker_list = [m for m in board.get_markers() if m != self.marker]
            opponent_marker = marker_list[0] if marker_list else ''

            score = self._score_move(move, opponent_marker, count_marks)
            # trace(score)
            if score > best:
                pick = move
                best = score
        return board.place_marker(pick, self.marker)

    # def _count_across_down(self):
    #     """
    #     for each row, col count the number of marks (for each player)
    #     """
    #     count_rows = {}
    #     count_cols = {}
    #     for row, col in itertools.product(range(self.size), range(self.size)):
    #         mark = self.board[row][col]
    #         try:
    #             count_rows[(row, mark)] = count_rows[(row, mark)] + 1
    #         except KeyError:
    #             count_rows[(row, mark)] = 1
    #         try:
    #             count_cols[(col, mark)] = count_cols[(col, mark)] + 1
    #         except KeyError:
    #             count_cols[(col, mark)] = 1
    #     return count_rows, count_cols

    # def _count_diagonal(self):
    #     """
    #     provides counts of the diagonal for each mark(player)
    #     """
    #     tally = {X: 0, O: 0, EMPTY: 0}
    #     count_diag1 = count_diag2 = tally.copy()
    #     for ndx in range(self.degree):
    #         # diag1 (0,0) (1,1) (2,2)
    #         mark = self.board[ndx][ndx]
    #         count_diag1[mark] = count_diag1[mark] + 1
    #
    #         # diag2 (0,2) (1,1) (2,0)
    #         mark = self.board[ndx][(self.degree - 1) - ndx]
    #         count_diag2[mark] = count_diag2[mark] + 1
    #     return count_diag1, count_diag2

    def _is_win(self, move, board):
        """
        sets the piece on a copy of the board to check for win
        """
        (row, col) = move
        #board = self.board.copy()
        board.board[row][col] = self.marker
        # trace(self.board)
        is_win = board.is_win(self.marker)
        board.board[row][col] = Board.EMPTY
        # trace(self.board)
        return is_win

    def _is_block(self, move, board):
        """
        checks to see if we would lose if the player went there
        """
        (row, col) = move
        # gets the list with our own marker taken out (0 or 1 element)
        marker_list = [m for m in board.get_markers() if m != self.marker]
        if marker_list:
            opponent_mark = marker_list[0]
            board.board[row][col] = opponent_mark
            is_loss = board.is_win(opponent_mark)
            board.board[row][col] = Board.EMPTY
            return is_loss
        return False


    def _score_move(self, move, opponent_marker, count_marks):
        """
        col score is looking at all the 'X', 'O' and EMPTY
        (assume 'computer is X')
        11 * how many X's + 10 * how many O's + 9 * how many opens
        """
        (row, col) = move
        ((count_rows, count_cols), (count_diag1, count_diag2)) = count_marks

        return (
            count_cols.get((col, self.marker), 0) * 11 +
            count_rows.get((row, self.marker), 0) * 11 +
            count_diag1.get(self.marker, 0) * 11 +
            count_diag2.get(self.marker, 0) * 11
            +
            count_cols.get((col, opponent_marker), 0) * 10 +
            count_rows.get((row, opponent_marker), 0) * 10 +
            count_diag1.get(opponent_marker, 0) * 10 +
            count_diag2.get(opponent_marker, 0) * 10
            +
            count_cols.get((col, Board.EMPTY), 0) * 11 +
            count_rows.get((row, Board.EMPTY), 0) * 11 +
            count_diag1.get(Board.EMPTY, 0) * 11 +
            count_diag2.get(Board.EMPTY, 0) * 11
        )

    def __repr__(self):
        return 'SmartPlayer({})'.format(self.marker)




def TicTacToe(mode=MODE, **args):
    """
    Game Object Generator Class - external Interface
    """
    # try:
    #     classname = 'TicTacToe' + mode
    #     classobj = eval(classname)
    # except:
    #     print('Bad -mode flag value:', mode)
    # return apply(eval(classname), (), args)



def main():
    """
    test method to call when invoked from main
    """
    # if len(sys.argv) == 1:
    #     TicTacToe().mainloop()
    # else:
    #     needEval = ['-degree']
    #     args = sys.argv[1:]
    #     opts = {}
    #     # parse the opts and args two at a time
    #     for i in range(0, len(args), +2):
    #         if args[i] in needEval:
    #             opts[args[i][1:]] = eval(args[i+1])
    #         else:
    #             opts[args[i][1:]] = args[i+1]
    #         trace(opts)
    #         apply(TicTacToe, (), opts).mainloop()
    series = Series()
    num_iterations = 10000
    print(f'run a series with {num_iterations} iterations')
    series.run(num_iterations)

    px = PlayerData('X', series.winning_moves)
    # Game().play([d1, p2])

    # series against trained opponent
    series2 = Series()
    print('run anotrher series with 1000')
    series2.run(100)
    po = PlayerData('O', series2.winning_moves)
    # pa1 = PlayerSmart('smrt1', 'X')
    # pa2 = PlayerSmart('smrt2', 'O')
    # Game().play([pa1, pa2])



if __name__ == '__main__':
    main()
