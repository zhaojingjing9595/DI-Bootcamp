
def display_board(current_board):
    print()
    print("Tic Tac Toe")
    print("*****************")
    for i in range(3):
        print(f"*  {current_board[i][0]}  | {current_board[i][1]} | {current_board[i][2]}   *")
        if i <= 2:
            print("*  ---|---|---  *")
    print("*****************")


def get_valid_num(row_or_col):
    while True:
        try:
            num = int(input(f"Enter {row_or_col}: "))
            if 1 <= num <= 3:
                break
            else:
                print("Number should be between 1 and 3")
        except ValueError:
            print("Invalid Number!")
    return num

def player_input(player, current_board, player_x, player_o ):
    print(f"Player {player}'s turn...")
    while True:
        row_number = get_valid_num("row")
        col_number = get_valid_num("column")
        # check if this position is occupied
        if current_board[row_number - 1][col_number - 1] is not " ":
            print("This position is occupied, please retry!")
        else:
            break
    
    current_board[row_number - 1][col_number - 1] = player
    if player == 'X':
        player_x.append( 3 * (row_number - 1) + col_number)
    else:
        player_o.append( 3 * (row_number - 1) + col_number)
    # return current_board

def check_winner(player, player_x, player_o):
    winner_cases = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [1, 5, 9],
        [3, 5, 7]
    ]
    
    player_moves = player_x if player == "X" else player_o
    for case in winner_cases:
        if set(case).issubset(player_moves):
            print(f"player {player} wins!")
            return True
    
    return False
            

def main():
    current_game = [[" " for col in range(3)] for row in range(3)]
    player_x = []
    player_o = []
    has_winner = False
    current_player = "X"
    print("Welcome to TIC TAC TOE!")
    move = 0
    while not has_winner and move <= 8:
        move += 1
        print(f"move {move}: ")
        display_board(current_game)
        player_input(current_player, current_game, player_x, player_o)
        has_winner = check_winner(current_player, player_x, player_o)
        current_player = "O" if current_player == "X" else "X"
        if not has_winner and move == 9:
            print("")
            print("It's a draw!")
    
    display_board(current_game)
        
main()