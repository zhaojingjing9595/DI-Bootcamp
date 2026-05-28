
from game import Game
def get_user_menu_choice():
    print("")
    print("Please select: ")
    print("")
    print("1. Play a new game")
    print("2. Show scores")
    print("3. Quit")
    print("")
    
    while True:
        try:
            user_choice = int(input("--->  "))
            if user_choice in [1, 2, 3]:
                break
            print(f"No option {user_choice}")
        except ValueError:
            print("Invalid option!")
        print("")
    
    return user_choice



def print_results(results):
    print("Here are the results: ")
    print(f"Wins: {results['win']}, Losses: {results['lose']}, draw: {results['draw']}")
    print("")
    

def main():
    print('************************************')
    print('Welcome to Rock, Paper and Scissors!')
    print('************************************')
    
    results = {'win': 0, 'lose': 0, 'draw': 0}
    while True:
        user_choice = get_user_menu_choice()
        if user_choice == 3:
            print_results(results)
            print("Thank you for playing! See you again!")
            break
        
        if user_choice == 2:
            print_results(results)
            
        if user_choice == 1:
            new_game = Game()
            result = new_game.play()
            if result == 'win':
                results['win'] += 1
            elif result == 'lose':
                results['lose'] += 1
            else:
                results['draw'] += 1

if __name__ == "__main__":
    main()