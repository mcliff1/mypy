#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Tic Tac Toe OO game
"""
import logging
#import random

from board import Board
from player import Player

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

# class Player():
#     """
#     represents a random player
#
#     a player shouldn't have a marker? or should they
#
#     made this a super class and sub with real person and various AI's
#     """
#
#     def __init__(self, marker):
#         """
#         it is expected to be either 'X' or 'O' for this game,
#         as long as the two players have separate markers
#
#         We have name so that we can use different implementations X or O
#         """
#         self.marker = marker
#         # since we use random, lets seed it now
#         random.seed()
#
#     def move(self, board):
#         """
#         return true if the move is made
#          otherwise return false if unable to move
#         """
#         #return board.place_marker((0, 0), self.marker)
#         open_moves = list(board.list_open_positions())
#         if open_moves:
#             move = random.choice(open_moves)
#             return board.place_marker(move, self.marker)
#         # else no open moves
#         return False
#
#
#     def __repr__(self):
#         return '{}'.format(self.marker)


class Game():
    """
    a board, and set of rules
     method play takes the players and runs the game

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



    #def play(self, player1, player2, trace=True):
    def play(self, players, trace=True):
        """
        trace option to draw the screen after each move (otherwise no display)


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
        player1 = players[0]
        player2 = players[1]
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


    def encode_win(self):
        """
        on a completed game with a winner
        returns tuple  the board status with winner-encoding (winning mark is 1)
        along with the move that was made
        """
        if not self.winner:
            # draw returns empty list
            return []

        return [(Board.encode(turn[2], turn[0]), turn[1])
                for turn in self.history()
                if turn[0] == self.winner.marker]

class Record:
    def __init__(self):
        self.player1 = 0
        self.player2 = 0
        self.draw = 0
    def __repr__(self):
        return 'player1 {}, player2 {}, draw {}'.format(self.player1, self.player2, self.draw)


class Series:
    """
    runs a series of games, recording their histories and
    record
    """

    def __init__(self, players=None):
        """
        by default will craete 2 random plays
        """
        self.game = Game()
        if players:
            self.player1 = players[0]
            self.player2 = players[1]
        else:
            self.player1 = Player('X')
            self.player2 = Player('O')
        self.record = Record()
        self.winning_moves = []

    def run(self, count=1, trace=False):
        """
        executes 'count' number of games updating the record
        """
        for _ in range(count):
            self.game.reset()
            self.game.play([self.player1, self.player2], trace=trace)
            self.winning_moves += self.game.encode_win()

            if not self.game.winner:
                self.record.draw += 1
            elif self.game.winner.marker == 'X':
                self.record.player1 += 1
            elif self.game.winner.marker == 'O':
                self.record.player2 += 1
        print(self.record)





def main():
    """
    test method to call when invoked from main
    """
    player1 = Player('X')
    player2 = Player('O')
    series = Series([player1, player2])
    series.run(100)

    series2 = Series()
    series2.run(2, trace=True)
    # pa1 = PlayerSmart('smrt1', 'X')
    # pa2 = PlayerSmart('smrt2', 'O')
    # Game().play([pa1, pa2])



if __name__ == '__main__':
    main()
