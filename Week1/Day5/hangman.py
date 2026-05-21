# Use python to create a Hangman game.

# Instructions
# The computer choose a random word and mark stars for each letter of each word.
# Then the player will guess a letter.
# If that letter is in the word(s) then the computer fills the letter in all the correct positions of the word.
# If the letter isn’t in the word(s) then add a body part to the gallows (head, body, left arm, right arm, left leg, right leg).
# The player will continue guessing letters until they can either solve the word(s) (or phrase) or all six body parts are on the gallows.
# The player can’t guess the same letter twice.


# Starter code
# Here is a piece of code that will give you a random word.
def guess_letter():
    while True:
        letter = input(f"Guess a letter : ").lower().strip()
        if len(letter) == 1 and letter.isalpha():
            return letter
        else:
            print("Not valid letter!")


def main():
    body_parts = ['head', 'body', 'left arm', 'right arm', 'left leg', 'right leg']
    words_list = ['correction', 'childish', 'beach', 'python', 'assertive', 'interference', 'complete', 'share', 'credit card', 'rush', 'south']
    word = random.choice(words_list) 

    displayed_word = ["x"] * len(word)
    guessed = []
    gallows = []
    
    while len(gallows) <= 5 and "".join(displayed_word) != word:
        print('')
        print(f"This is the word: {''.join(displayed_word)}")
        letter = guess_letter()
        if letter in guessed:
            print(f"You guessed {letter} already! Please choose a new letter!")
            continue
        
        guessed.append(letter) 
        if letter not in word:
            body_part = body_parts.pop(0)
            gallows.append(body_part)
            print(f"Wrong guess! Adding a {body_part} into the gallows.")
        else:
            for i, char in enumerate(word):
                if char == letter:
                    displayed_word[i] = letter
    if "".join(displayed_word) == word:
        print(f"Congrats! You guessed the word: {word}!")
    else:
        print(f"You failed! The word is {word}")

import random
main()