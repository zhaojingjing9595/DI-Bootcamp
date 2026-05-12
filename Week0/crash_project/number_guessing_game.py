import random

def number_guessing_game():
    random_number = random.randint(1, 100)
    max_attempts = 7
    
    for i in range(max_attempts):
        label = "Last Attempt" if i == max_attempts - 1 else f"Attempt {i + 1}"
        user_input = input(f"{label} - Enter a number: ")
        try:
            number = int(user_input)
            if number == random_number:
                print("You guessed right!")
                break
            elif number > random_number:
                print("Too High!")
            else:
                print("Too Low!")
        except ValueError:
            print("This is not a valid integer")
    else:
        print(f"Out of attempts! The correct number was {random_number}.")
            
        

if __name__ == "__main__":
    number_guessing_game()