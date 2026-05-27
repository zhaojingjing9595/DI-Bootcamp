from anagram_checker import AnagramChecker

checker = AnagramChecker('sowpods.txt')

def input_valid_word(user_input):
    # Remove whitespace from start and end
    word = user_input.strip()

    # Check if user typed more than one word
    if len(word.split()) != 1:
        print("Error: Please enter only one word.")
        return None

    # Check if only alphabetic characters
    if not word.isalpha():
        print("Error: Only alphabetic characters are allowed.")
        return None
    return word

def main():
    while True:
        print("Please select:")
        print("")
        print("1. Input a word or text")
        print("2. exit")
        print("")
        
        try:
            selected = int(input('My selection is: '))
        except ValueError:
            print("")
            print("Invalid input! Please enter 1 or 2.")
            print("")
            continue
        
        if selected not in [1, 2]:
            print("")
            print("Invalid Input!")
            print("")
            continue
        
        if selected == 2:
            break
        
        if selected == 1:
            word = input("Enter Your word: ")
            valid_word = input_valid_word(word)
            if not valid_word:
                print("Invalid Word!")
                continue
            print("this is a valid English word.")
            anagrams = checker.get_anagrams(valid_word)
            print(f"Anagrams for your word: {", ".join(anagrams)}")
            break
            

main()
    
    