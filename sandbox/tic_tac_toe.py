# -*- coding: utf-8 -*-
"""
Text based Tic Tac Toe implementation

from https://github.com/solkaz/tic-tac-pytoe/blob/master/tic_tac_toe.py
"""
import random

BOARD = {
    'top-L' : ' ', 'top-M' : ' ', 'top-R': ' ',
    'mid-L' : ' ', 'mid-M' : ' ', 'mid-R': ' ',
    'bot-L' : ' ', 'bot-M' : ' ', 'bot-R': ' '
}
LAT = ['top-', 'mid-', 'bot-']
LON = ['L', 'M', 'R']

player_icon = ''
computer_icon = ''

def print_BOARD():
    """
    prints the current state of the BOARD to console
    """
    print(' ' + BOARD['top-L'] + ' | ' + BOARD['top-M'] + ' | ' + BOARD['top-R'])
    print('---+---+---')
    print(' ' + BOARD['mid-L'] + ' | ' + BOARD['mid-M'] + ' | ' + BOARD['mid-R'])
    print('---+---+---')
    print(' ' + BOARD['bot-L'] + ' | ' + BOARD['bot-M'] + ' | ' + BOARD['bot-R'])


def check_for_victory(is_player):
    """
    checks to see if the player (if true), computer (if false)
    is in a victory state on the BOARD
    """
    check_char = player_icon if is_player else computer_icon

    # check the horizontal rows
    for rows in range(len(LAT)):
        if (BOARD[LAT[rows] + LON[0]] == check_char and
                BOARD[LAT[rows] + LON[1]] == check_char and
                BOARD[LAT[rows] + LON[2]] == check_char):
            return True

    # check the verticals cols
    for cols in range(len(LON)):
        if (BOARD[LAT[0] + LON[cols]] == check_char and
                BOARD[LAT[1] + LON[cols]] == check_char and
                BOARD[LAT[2] + LON[cols]] == check_char):
            return True

    # check diagonal
    if (BOARD['mid-M'] == check_char and
            ((BOARD['top-L'] == check_char and BOARD['bot-R'] == check_char) or
             (BOARD['top-R'] == check_char and BOARD['bot-L'] == check_char))):
        return True

    # else no vicotry condition found
    return False
