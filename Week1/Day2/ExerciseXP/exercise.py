# 🌟 Exercise 1: Favorite Numbers
# Key Python Topics:

# Sets
# Adding/removing items in a set
# Set concatenation (using union)


# Instructions:

# Create a set called my_fav_numbers and populate it with your favorite numbers.
# Add two new numbers to the set.
# Remove the last number you added to the set.
# Create another set called friend_fav_numbers and populate it with your friend’s favorite numbers.
# Concatenate my_fav_numbers and friend_fav_numbers to create a new set called our_fav_numbers.
# Note: Sets are unordered collections, so ensure no duplicate numbers are added.
my_fav_numbers = {1, 2, 4}
my_fav_numbers.add(3)
my_fav_numbers.add(6)
my_fav_numbers.remove(6)
friend_fav_numbers = {4, 8, 9}
our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
print(our_fav_numbers)


# 🌟 Exercise 2: Tuple
# Key Python Topics:

# Tuples (immutability)


# Instructions:

# Given a tuple of integers, try to add more integers to the tuple.
# Hint: Tuples are immutable, meaning they cannot be changed after creation. Think about why you can’t add more integers to a tuple.
my_tuple = (1, 2, 3)
more_nums = (4, 5)
my_tuple += more_nums
print(my_tuple)

# 🌟 Exercise 3: List Manipulation
# Key Python Topics:

# Lists
# List methods: append, remove, insert, count, clear


# Instructions:

# You have a list: basket = ["Banana", "Apples", "Oranges", "Blueberries"]
# Remove "Banana" from the list.
# Remove "Blueberries" from the list.
# Add "Kiwi" to the end of the list.
# Add "Apples" to the beginning of the list.
# Count how many times "Apples" appear in the list.
# Empty the list.
# Print the final state of the list.
basket = ["Banana", "Apples", "Oranges", "Blueberries"]
basket.remove("Banana")
basket.remove("Blueberries")
basket.append("Kiwi")
basket.insert(0, "Apples")
count = basket.count("Apples")
basket.clear()
print(basket)

# 🌟 Exercise 4: Floats
# Key Python Topics:

# Lists
# Floats and integers
# Range generation


# Instructions:

# Recap: What is a float? What’s the difference between a float and an integer?
# Create a list containing the following sequence of mixed types: floats and integers:
# 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.
# Avoid hard-coding each number manually.
# Think: Can you generate this sequence using a loop or another method?

my_list = [1.5 + 0.5*i if i % 2 == 0 else int(1.5 + 0.5*i) for i in range(8)]
print(my_list)

# 🌟 Exercise 5: For Loop
# Key Python Topics:

# Loops (for)
# Range and indexing


# Instructions:

# Write a for loop to print all numbers from 1 to 20, inclusive.
# Write another for loop that prints every number from 1 to 20 where the index is even.
for i in range(1, 21):
    print(i)
 
    
for i in range(1, 21):
    if i % 2 != 0:
        print(i)

# 🌟 Exercise 6: While Loop
# Key Python Topics:

# Loops (while)
# Conditionals


# Instructions:

# Use an input to ask the user to enter their name.
# Using a while True loop, check if the user gave a proper name (not digits and at least 3 letters long)
# hint: check for the method isdigit()
# if the input is incorrect, keep asking for the correct input until it is correct
# if the input is correct print “thank you” and break the loop
while True:
    name = input("Enter your name: ")
    
    if len(name) < 3:
        print("Name should be at least 3 letters long!")
    elif any(char.isdigit() for char in name):
        print("Name shouldn't have digit inside!")
    else:
        print("thank you")
        break

# 🌟 Exercise 7: Favorite Fruits
# Key Python Topics:

# Input/output
# Strings and lists
# Conditionals


# Instructions:

# Ask the user to input their favorite fruits (they can input several fruits, separated by spaces).
# Store these fruits in a list.
# Ask the user to input the name of any fruit.
# If the fruit is in their list of favorite fruits, print:
# "You chose one of your favorite fruits! Enjoy!"
# If not, print:
# "You chose a new fruit. I hope you enjoy it!"
fav_fruits = input("Enter a list of your favorite fruits, separated by space: ")
fav_fruits_list = fav_fruits.lower().split()
chosen_fruit = input("choose a fruit: ").strip().lower()
if chosen_fruit in fav_fruits_list:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")

# 🌟 Exercise 8: Pizza Toppings
# Key Python Topics:

# Loops
# Lists
# String formatting


# Instructions:

# Write a loop that asks the user to enter pizza toppings one by one.
# Stop the loop when the user types 'quit'.
# For each topping entered, print:
# "Adding [topping] to your pizza."
# After exiting the loop, print all the toppings and the total cost of the pizza.
# The base price is $10, and each topping adds $2.50.

list_toppings = []
while True:
    topping = input("please enter a topping for your pizza: ")
    if topping.lower() == "quit":
        print(f"Your pizza toppings are: {", ".join(list_toppings)}, the total amount is ${10 + 2.5 * len(list_toppings)}")
        break
    
    list_toppings.append(topping)
    print(f"Adding {topping} to your pizza")
    
# 🌟 Exercise 9: Cinemax Tickets
# Key Python Topics:

# Conditionals
# Lists
# Loops


# Instructions:

# Ask for the age of each person in a family who wants to buy a movie ticket.
# Calculate the total cost based on the following rules:
# Free for people under 3.
# $10 for people aged 3 to 12.
# $15 for anyone over 12.
# Print the total ticket cost.

total_cost = 0
while True:
    try:
        num_people = int(input("How many family members? "))
        break
    except ValueError:
        print("Please enter an integer number!")
for i in range(1, num_people + 1):
    age = int(input(f"Family member {i}: What's the age? "))
    
    if age < 3:
        ticket_cost = 0
    elif 3 <= age <= 12:
        ticket_cost = 10
    else: 
        ticket_cost = 15
    
    total_cost += ticket_cost

print(f"Total ticket costs: ${total_cost}")
        
    