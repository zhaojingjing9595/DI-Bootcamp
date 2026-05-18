# Instructions:
# 1. Ask for User Input:

# The string must be exactly 10 characters long.
# 2. Check the Length of the String:

# If the string is less than 10 characters, print: "String not long enough."
# If the string is more than 10 characters, print: "String too long."
# If the string is exactly 10 characters, print: "Perfect string" and proceed to the next steps.
# 3. Print the First and Last Characters:

# Once the string is validated, print the first and last characters.
# 4. Build the String Character by Character:

# Using a for loop, construct and print the string character by character. Start with the first character, then the first two characters, and so on, until the entire string is printed.
# Hint: You can create a loop that goes through the string, adding one character at a time, and print it progressively.

# Example:

# Alt text

# 5. Bonus: Jumble the String (Optional)

# As a bonus, try shuffling the characters in the string and print the newly jumbled string.
# Hint: You can use the random.shuffle function to shuffle a list of characters.
import random
length = 0
while length != 10:
    user_input=input("Please input a string (10 char long): ")
    length = len(user_input)
    if length > 10:
        print("String too long.")
    elif length < 10:
        print("String not long enough.")
    else:
        print("Perfect string!")

print("first char: ", user_input[0])
print("last char: ", user_input[-1])

print_str=""
for i in range(length):
    print_str+=user_input[i]
    print(print_str)

user_input_list=list(user_input)
random.shuffle(user_input_list)
new_str="".join(user_input_list)
print(new_str)
    
    