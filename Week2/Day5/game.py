import random

class Game:
    rock = 'rock'
    paper = 'paper'
    scissors = 'scissors'
    items = [rock, paper, scissors]
    
    def __init__(self):
        pass
    
    def get_user_item(self):
        while True:
            print("")
            user_item = input("Please choose from rock, paper or scissors: ").strip()
            print("")
            
            if user_item in Game.items:
                break
            
            print("That's not an option! Only rock, paper or scissors!")
            
        return user_item    
        
    def get_computer_item(self):
        computer_choice = random.choice(Game.items)
        return computer_choice
    
    def get_game_result(self, user_item, computer_item):
        if user_item == computer_item:
            return "draw"
        
        if user_item == Game.rock and computer_item == Game.scissors:
            return "win"
            
        if user_item == Game.scissors and computer_item == Game.paper:
            return "win"
        
        if user_item == Game.paper and computer_item == Game.rock:
            return "win"
        
        return "lose"
    
    def play(self):
        print("Let's start the game!!!!")
        
        # get user item
        user_choice = self.get_user_item()
        # get computer item
        computer_choice = self.get_computer_item()
        # show result
        result = self.get_game_result(user_choice, computer_choice)
        print(f"You chose: {user_choice}, computer chose {computer_choice}.")
        if result == 'win':
            print("You win!")
        elif result == 'lose':
            print("You lost :(")
        else:
            print("It's a draw.")
        
        return result
        
        
