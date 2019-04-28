#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Tic Tac Toe OO game
"""
import logging
import random

#from board import Board

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

class Player():
    """
    represents a random player

    a player shouldn't have a marker? or should they

    made this a super class and sub with real person and various AI's
    """

    def __init__(self, marker):
        """
        it is expected to be either 'X' or 'O' for this game,
        as long as the two players have separate markers

        We have name so that we can use different implementations X or O
        """
        self.marker = marker
        # since we use random, lets seed it now
        random.seed()

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
        return '{}'.format(self.marker)


def main():
    """
    test method to call when invoked from main
    """
    player1 = Player('X')
    player2 = Player('O')

if __name__ == '__main__':
    main()
