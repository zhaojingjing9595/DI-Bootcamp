# 🌟 Exercise 1: Cats
# Key Python Topics:

# Classes and objects
# Object instantiation
# Attributes
# Functions

# Instructions:

# Use the provided Cat class to create three cat objects. Then, create a function to find the oldest cat and print its details.
# Step 1: Create Cat Objects
# Use the Cat class to create three cat objects with different names and ages.

# Step 2: Create a Function to Find the Oldest Cat
# Create a function that takes the three cat objects as input.
# Inside the function, compare the ages of the cats to find the oldest one.
# Return the oldest cat object.


# Step 3: Print the Oldest Cat’s Details

# Call the function to get the oldest cat.
# Print a formatted string: “The oldest cat is <cat_name>, and is <cat_age> years old.”
# Replace <cat_name> and <cat_age> with the oldest cat’s name and age.


# Example:

class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age

# # Step 1: Create cat objects
cat1 = Cat("Mochi", 10)
cat2 = Cat("Macha", 2)
cat3 = Cat("Mocha", 13)

# # Step 2: Create a function to find the oldest cat
def find_oldest_cat(cat1, cat2, cat3):
    # ... code to find and return the oldest cat ...
    oldest_cat = cat1
    if oldest_cat.age < cat2.age:
        oldest_cat = cat2
    if oldest_cat.age < cat3.age:
        oldest_cat = cat3
    # Step 3: Print the oldest cat's details
    print(f"the oldest cat is {oldest_cat.name} and her age is {oldest_cat.age}")
find_oldest_cat(cat1, cat2, cat3)

# 🌟 Exercise 2 : Dogs
# Goal: Create a Dog class, instantiate objects, call methods, and compare dog sizes.
# Key Python Topics:
# Classes and objects
# Object instantiation
# Methods
# Attributes
# Conditional statements (if)
# Instructions:

# Create a Dog class with methods for barking and jumping. Instantiate dog objects, call their methods, and compare their sizes.

# Step 1: Create the Dog Class

# Create a class called Dog.
# In the __init__ method, take name and height as parameters and create corresponding attributes.
# Create a bark() method that prints “<dog_name> goes woof!”.
# Create a jump() method that prints “<dog_name> jumps <x> cm high!”, where x is height * 2.
class Dog:
    def __init__(self, name, height):
        self.name = name
        self.height = height
    
    def bark(self):
        print(f"{self.name} goes woof!")
    
    def jump(self):
        print(f"{self.name} jumps {self.height * 2} cm high!")

# Step 2: Create Dog Objects

# Create davids_dog and sarahs_dog objects with their respective names and heights.
davids = Dog("Davis", 32)
sarah = Dog("Sarah", 45)

# Step 3: Print Dog Details and Call Methods

# Print the name and height of each dog.
# Call the bark() and jump() methods for each dog.
print(f"{davids.name} is {davids.height} cm high.")
davids.bark()
davids.jump()
print(f"{sarah.name} is {sarah.height} cm high.")
sarah.bark()
sarah.jump()
# Step 4: Compare Dog Sizes
if davids.height > sarah.height:
    print(f"{davids.name} is higher than {sarah.name}")
elif sarah.height > davids.height:
    print(f"{sarah.name} is higher than {davids.name}")
else:
    print(f"{sarah.name} and {davids.name} are equally high.")
    
# 🌟 Exercise 3 : Who’s the song producer?
# Goal: Create a Song class to represent song lyrics and print them.
# Key Python Topics:

# Classes and objects
# Object instantiation
# Methods
# Lists


# Instructions:

# Create a Song class with a method to print song lyrics line by line.



# Step 1: Create the Song Class

# Create a class called Song.
# In the __init__ method, take lyrics (a list) as a parameter and create a corresponding attribute.
# Create a sing_me_a_song() method that prints each element of the lyrics list on a new line.
class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics
        
    def sing_me_a_song(self):
        for line in self.lyrics:
            print(f"{line}")
        

# Example:

stairway = Song(["There’s a lady who's sure", "all that glitters is gold", "and she’s buying a stairway to heaven"])

stairway.sing_me_a_song()

# Output: There’s a lady who’s sureall that glitters is goldand she’s buying a stairway to heaven


# 🌟 Exercise 4 : Afternoon at the Zoo
# Goal:

# Create a Zoo class to manage animals. The class should allow adding animals, displaying them, selling them, and organizing them into alphabetical groups.
# Key Python Topics:

# Classes and objects
# Object instantiation
# Methods
# Lists
# Dictionaries (for grouping)
# String manipulation


# Instructions
# Step 1: Define the Zoo Class
# 1. Create a class called Zoo.
class Zoo():
    # 2. Implement the __init__() method:
    # It takes a string parameter zoo_name, representing the name of the zoo.
    # Initialize an empty list called animals to keep track of animal names.
    def __init__(self, zoo_name):
        self.zoo_name = zoo_name
        self.animals = []

    # 3. Add a method add_animal(new_animal):
    # This method adds a new animal to the animals list.
    # Do not add the animal if it is already in the list.
    def add_animal(self, new_animal):
        if new_animal not in self.animals:
            self.animals.append(new_animal)
        

    # 4. Add a method get_animals():
    # This method prints all animals currently in the zoo.
    def get_animals(self):
        print(f"all animals currently in the zoo: {", ".join(self.animals)}")
        
    # 5. Add a method sell_animal(animal_sold):
    # This method checks if a specified animal exists on the animals list and if so, remove from it.
    def sell_animal(self, animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)
            
    # 6. Add a method sort_animals():
    # This method sorts the animals alphabetically.
    # It also groups them by the first letter of their name.
    # The result should be a dictionary where:
    # Each key is a letter.
    # Each value is a list of animals that start with that letter.
    # Example output:

    # {
    #    'B': ['Baboon', 'Bear'],
    #    'C': ['Cat', 'Cougar'],
    #    'G': ['Giraffe'],
    #    'L': ['Lion'],
    #    'Z': ['Zebra']
    # }
    def sort_animals(self):
        self.animals.sort()
        result = {}
        for animal in self.animals:
            if animal[0].upper() not in result.keys():
                result[animal[0].upper()] = [animal.capitalize()]
            else:
                result[animal[0].upper()].append(animal.capitalize())
        print(result)
        return result
        
    # 7. Add a method get_groups():
    # This method prints the grouped animals as created by sort_animals().
    # Example output:

    # B: ['Baboon', 'Bear']
    # C: ['Cat', 'Cougar']
    # G: ['Giraffe']
    # ...
    def get_groups(self):
        grouped_animals = self.sort_animals()
        for key, value in grouped_animals.items():
            print(f"{key}: {value}") 
        
        
# Step 2: Create a Zoo Object
# Create an instance of the Zoo class and pass a name for the zoo.
tlv_zoo = Zoo("Tel Aviv Zoo")

# Step 3: Call the Zoo Methods
# Use the methods of your Zoo object to test adding, selling, displaying, sorting, and grouping animals.
tlv_zoo.add_animal("bear")
tlv_zoo.add_animal("monkey")
tlv_zoo.add_animal("bird")
tlv_zoo.add_animal("elephant")
tlv_zoo.add_animal("snake")

tlv_zoo.get_animals()
tlv_zoo.sell_animal("dog")
tlv_zoo.sell_animal("monkey")
tlv_zoo.get_animals()
tlv_zoo.sort_animals()
tlv_zoo.get_groups()

# Bonus: Modify the add_animal() method to get *args so you dont need to repeat the method each time for a new animal, you can pass multiple animals names separated by a comma.

def add_animal(self, *animals):
    for i in list(animals):
        if i not in self.animals:
            self.animals.append(i)

Zoo.add_animal = add_animal

tlv_zoo.add_animal("turtle", "panda")
tlv_zoo.get_animals()