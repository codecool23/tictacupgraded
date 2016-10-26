import os
import random
import sys

board = [" ", " ", " ",
         " ", " ", " ",
         " ", " ", " "]

players = [" ", " "]

wins = [[0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 4, 8], [2, 4, 6]]

player2_wins = False


def show_instructions():
    print("Use the numbers to make your move! ")
    print()
    print (1, '|', 2, '|', 3)
    print ('---------')
    print (4, '|', 5, '|', 6)
    print ('---------')
    print (7, '|', 8, '|', 9)


def play_mode_selection():
    print("Menu")
    print("--------------------------------------------")
    print("Choose what kind of game you want to play: ")
    print("1:Two Payer game mode")
    print("2:Player Vs AI mode")
    print("--------------------------------------------")
    print("3:QUIT")
    user_input = ""
    while (user_input != "1" and user_input != "2" and user_input != "3"):
        user_input = input(
            "Choose from the numbers (write 1, 2 or 3 and press ENTER): ")
    if "1" == user_input:
        two_player_mode()
        return 1
    if "2" == user_input:
        ai_mode()
        return 2
    if "3" == user_input:
        sys.exit()


def get_player_names():
    print()
    players[0] = input("Enter name for player1: ").title()
    players[1] = input("Enter name for player2: ").title()
    print()
    print(players[1] + " goes first with O, " + players[0] + " is with X")
    print()


def show_game():
    ''' Prints out the actual playground '''
    print (board[0], '|', board[1], '|', board[2])
    print ('---------')
    print (board[3], '|', board[4], '|', board[5])
    print ('---------')
    print (board[6], '|', board[7], '|', board[8])
    print()


def new_board():
    global board
    board = [" ", " ", " ",
             " ", " ", " ",
             " ", " ", " "]


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def make_red(char):
    if os.name == 'nt':
        return char
    else:
        return "\u001b[1;31m" + char + "\u001b[0m"


def print_winner(winner_player):
    print(winner_player + make_red(" won") + "!")


def make_winner_combo_red(char, spot1, spot2, spot3):
    '''If there is a winner combo, it will make the 3 winner symbol red'''
    board[spot1] = make_red(char)
    board[spot2] = make_red(char)
    board[spot3] = make_red(char)
    show_game()


def print_and_update_winner(char):
    global player2_wins
    if char == "X":
        print_winner(players[0])
        player2_wins = False
    if char == "O":
        print_winner(players[1])
        player2_wins = True


def play_again():
    '''Player can select from options
    y - play again
    n - back to the menu
    q - exit program'''
    print("Available moves: play again (y), back to the menu (n), exit program (q)")
    again = input("Choose your next move (y,n,q): ")
    if again == "y":
        new_board()
    elif again == "q":
        print("Until the next time,bye!")
        sys.exit()
    elif again == "n":
        game()


def win_combo(char, spot1, spot2, spot3):
    '''In case of winning it turns the winning combination red,
    prints out the winner, and gives the chance to start over.'''
    if board[spot1] == char and board[spot2] == char and board[spot3] == char:
        make_winner_combo_red(char, spot1, spot2, spot3)
        print_and_update_winner(char)
        play_again()


def is_there_space():
    '''Decides if the board is full in the 2 player game'''
    board_state = False
    for i in range(len(board)):
        if " " in board[1:9]:
            board_state = True
        else:
            print("It's a tie!")
            print()
            new_board()
            one_round()
    return board_state


def is_there_space_ai():
    '''Decides if the board is full in the ai mode'''
    board_state_ai = False
    for i in range(len(board)):
        if " " in board[1:9]:
            board_state_ai = True
        else:
            print("It's a tie!")
            print()
            new_board()
            move_against_ai()
    return board_state_ai


def check_winning(char):
    winning = 0
    for x in range(len(wins)):
        win_combo(char, wins[x][0], wins[x][1], wins[x][2])


def is_valid_move(candidate):
    found_valid_move = False
    if int(candidate) >= 0 and int(candidate) < 9:
        found_valid_move = True
    return found_valid_move


def input_safe_digit(message):
    '''Decides if the input is a digit'''
    candidate = input(message)
    while not candidate.isdigit():
        print("Enter a valid number!")
        candidate = input(message)
    return candidate


def move_two_player(player, symbol, other_symbol, next_player_move):
    ''' Defines moves in the two-player mode. '''
    while is_there_space() is True:
        move = input_safe_digit(player + " make your move ("+symbol+"): ")
        move = int(move)-1
        if is_valid_move(move) is True:
            if board[int(move)] != symbol and board[int(move)] != other_symbol:
                board[(int(move))] = symbol
                check_winning(symbol)
                clear()
                show_instructions()
                print()
                print()
                show_game()
                next_player_move()
            else:
                print("Taken")
        else:
            print("Invalid move")


def move_against_ai():
    ''' Defines moves in the ai-mode '''
    while is_there_space_ai() is True:
        move = input_safe_digit(players[0] + ", please choose a spot (1-9): ")
        move = int(move)-1
        if is_valid_move(move) is True:
            if board[int(move)] != 'X' and board[int(move)] != 'O':
                board[(int(move))] = 'X'
                check_winning("X")
                finding = True
                while finding is True:
                    random.seed()
                    opponent = random.randint(0, 8)
                    if board[opponent] != 'O' and board[opponent] != 'X':
                        board[opponent] = 'O'
                        check_winning("O")
                        finding = False
                        clear()
                        show_instructions()
                        print()
                        print()
                        show_game()
            else:
                print("This spot is taken!")
        else:
            print("Invalid move")


def player1_move():
    move_two_player(players[0], "X", "O", player2_move)


def player2_move():
    move_two_player(players[1], "O", "X", player1_move)


def next_move():
    if player2_wins is False:
        player2_move()
        player1_move()
    else:
        player1_move()
        player2_move()


def one_round():
    show_game()
    next_move()
    check_winning()


def two_player_mode():
    get_player_names()
    new_board()
    one_round()


def ai_mode():
    players[0] = input("Enter name for player: ").title()
    players[1] = "Computer"
    new_board()
    show_game()
    move_against_ai()


def game():
    print("Welcome to TicTacToe!")
    print()
    play_mode_selection()
    show_instructions()
    two_player_mode()
    ai_mode()
game()
