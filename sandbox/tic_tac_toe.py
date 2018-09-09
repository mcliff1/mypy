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


def print_board():
    """
    prints the current state of the BOARD to console
    """
    # print()
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
    #global player_icon
    #global computer_icon
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


def player_move():
    """
    prompts the user to make a move

    returns True if the move results in a win
    """
    print('Please select where to place your piece: ', end='')
    has_played = False
    # ensure a valid move is selected
    while not has_played:
        choice = input() # input in form of 'bot-R', etc
        while not validate_player_input(choice):
            print('Invalid input, try again using {top|mid|bot}-{L|M|R} (e.g. top-L): ', end='')
            choice = input()
        # ensure the location is available
        if check_if_played(choice):
            print('a piece is already in that locaation, select another: ', end='')
        else:
            print('setting {} to be {}'.format(choice, player_icon))
            BOARD[choice] = player_icon
            has_played = True
    print_board()

    return check_for_victory(is_player=True)

def computer_move():
    """
    randomly select a spot

    returns true if the move results in a victory
    """
    rand_row = random.randint(0, 2)
    rand_col = random.randint(0, 2)

    while check_if_played(LAT[rand_row] + LON[rand_col]):
        rand_row = random.randint(0, 2)
        rand_col = random.randint(0, 2)

    print('setting {} to be {}'.format(LAT[rand_row]+LON[rand_col], computer_icon))

    BOARD[LAT[rand_row] + LON[rand_col]] = computer_icon
    print_board()

    return check_for_victory(is_player=False)


def validate_player_input(player_input):
    """
    the input string needs to be one of the field labels
    """
    for i in BOARD.keys():
        if player_input == str(i):
            return True
    return False


def check_if_played(selected_field):
    """
    checks to see if the field input is already selected
    """
    return not BOARD[selected_field] == ' '


def main():
    """
    main application
    """
    global player_icon
    global computer_icon
    print('Welcom to tic-tac-toe, select Heads or Tails to see who goes first')
    answer = input().lower()
    while not answer or (answer[0] != 'h' and answer[0] != 't'):
        print('Please enter heads or tails')
        answer = input().lower()
    random.seed()
    coin_flip = random.randint(1, 2)
    if ((answer[0] == 'h' and coin_flip == 1) or
            (answer[0] == 't' and coin_flip == 2)):
        print('you are X')
        player_icon = 'X'
        computer_icon = 'O'
    else:
        print('you are O')
        player_icon = 'O'
        computer_icon = 'X'

    move_count = 0
    winner = None
    print_board()
    while move_count != 9:
        if player_icon == 'X':
            if player_move():
                winner = 'player'
                break
            print()
            if computer_move():
                winner = 'computer'
                break
        else:
            # player is 'O'
            if computer_move():
                winner = 'computer'
                break
            print()
            if player_move():
                winner = 'player'
                break
        print()
        move_count += 1

    # if we don't have a winner at 9 moves, it's a tie
    if move_count == 9 and not winner:
        print('tie game')
    else:
        if winner == 'player':
            print('You Win!')
        else:
            print('Sorry, you lost')

if __name__ == '__main__':
    main()
