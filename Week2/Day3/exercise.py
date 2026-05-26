# Try to create a countdown to your birthday !

# For example : "My birthday is in 45 days, and 10:29:46"

from datetime import datetime, date

now = datetime.now()
print(now)

my_birthday = "05/09/2026"
bd = datetime.strptime(my_birthday, "%d/%m/%Y")
print(bd)

countdown = bd - now
print(countdown)
print(f"My birthday is in {str(countdown).replace("," , "and")}")


# 🌟 Exercise 1: Currencies
# Goal: Implement dunder methods for a Currency class to handle string representation, integer conversion, addition, and in-place addition.
# Key Python Topics:
# Dunder methods (__str__, __repr__, __int__, __add__, __iadd__)
# Type checking (isinstance())
# Raising exceptions (raise TypeError)


# Instructions:
class Currency:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount

    #Your code starts HERE
    def __str__(self):
        return f"{self.amount} {self.currency}{'s' if self.amount > 1 else ''}"
    def __int__(self):
        try:
            return int(self.amount)
        except ValueError:
            print("amount must be an int!")
            return 0
    
    def __repr__(self):
        return str(self)
        
    
    def __add__(self, other):
        if isinstance(other, int):
            return Currency(self.currency, self.amount + other)
        
        if isinstance(other, Currency):
            # check if they are the same currency
            if other.currency != self.currency:
                raise TypeError(
                    f"Cannot add between Currency type {self.currency} and {other.currency}"
                )
                
            return Currency(self.currency, other.amount + self.amount)
        
        raise TypeError(
            f"Cannot add Currency with {type(other).__name__}"
        )
       
            
        
    
            
    
# Using the code above, implement the relevant methods and dunder methods which will output the results below.

# Hint : When adding 2 currencies which don’t share the same label you should raise an error.

c1 = Currency('dollar', 5)
c2 = Currency('dollar', 10)
c3 = Currency('shekel', 1)
c4 = Currency('shekel', 10)

# #the comment is the expected output
print(c1)
# # '5 dollars'

print(int(c1))
# # 5

print(repr(c1))
# # '5 dollars'

print(c1 + 5)
# # 10

print(c1 + c2)
# # 15

print(c1) 
# # 5 dollars

c1 += 5
print(c1)
# # 10 dollars

c1 += c2
print(c1)
# # 20 dollars

# print(c1 + c3)
# # TypeError: Cannot add between Currency type <dollar> and <shekel>
# #comment the print above before you run the file for next exercises (since the error will crash your file)


# 🌟 Exercise 2: Import
# Goal: Create a module with a function and import it into another file.

# Instructions:
# Create a func.py file with a function that sums two numbers and prints the result. Then, import and call the function from exercise_one.py.
# Key Python Topics:

# Modules (creating and importing)
# Functions


# Step 1: Create func.py

# Create a file named func.py.
# Define a function inside that file that takes two numbers as arguments, sums them, and prints the result.

from func import sum
# Step 2: Create exercise_one.py

# Create a file named exercise_one.py.
# Import the function from func.py using one of the import syntaxes provided in the instructions.
# Call the imported function with two numbers.
print(sum(1, 2))


# 🌟 Exercise 3: String module
# Goal: Generate a random string of length 5 using the string module.

# Instructions:
# Use the string module to generate a random string of length 5, consisting of uppercase and lowercase letters only.

# Key Python Topics:

# string module
# random module
# String concatenation


# Step 1: Import the string and random modules

# Import the string and random modules.
import string, random

# Step 2: Create a string of all letters
letters = string.ascii_lowercase
print(letters)
# Read about the strings methods HERE to find the best methods for this step

# Step 3: Generate a random string

# Use a loop to select 5 random characters from the combined string.
# Concatenate the characters to form the random string.
random_str = ''
for i in range(5):
    letter = random.choice(letters)
    print(letter)
    random_str += letter
    
print(random_str)
    

# 🌟 Exercise 4: Current Date
# Goal: Create a function that displays the current date.

# Key Python Topics:

# datetime module
# Instructions:

# Use the datetime module to create a function that displays the current date.

# Step 1: Import the datetime module
# import already
# Step 2: Get the current date
current_date = datetime.now()
# Step 3: Display the date
print(current_date)


# 🌟 Exercise 5: Amount of time left until January 1st
# Goal: Create a function that displays the amount of time left until January 1st.

# Key Python Topics:

# datetime module
# Time difference calculations


# Instructions:

# Use the datetime module to calculate and display the time left until January 1st.
# more info about this module HERE

# Step 1: Import the datetime module

# Step 2: Get the current date and time
now = datetime.now()
print(now)
# Step 3: Create a datetime object for January 1st of the next year
new_year = datetime.strptime('01/01/2027', "%d/%m/%Y")
# Step 4: Calculate the time difference
diff = new_year - now
# Step 5: Display the time difference
print(diff)

# 🌟 Exercise 6: Birthday and minutes
# Key Python Topics:

# datetime module
# datetime.datetime.strptime() (parsing dates)
# Time difference calculations
# .total_seconds() method


# Instructions:
# Create a function that accepts a birthdate as an argument (in the format of your choice), then displays a message stating how many minutes the user lived in his life.
def lived_in_mins(birthday):
    bd = datetime.strptime(birthday, "%d/%m/%Y")
    diff = datetime.now() - bd
    return diff.total_seconds()

print(lived_in_mins('05/09/1995'))
    


# 🌟 Exercise 7: Faker Module
# Goal: Use the faker module to generate fake user data and store it in a list of dictionaries.
# Read more about this module HERE

# Key Python Topics:

# faker module
# Dictionaries
# Lists
# Loops


# Instructions:

# Install the faker module and use it to create a list of dictionaries, where each dictionary represents a user with fake data.

# Step 1: Install the faker module

# Step 2: Import the faker module

# Step 3: Create an empty list of users

# Step 4: Create a function to add users

# Create a function that takes the number of users to generate as an argument.
# Inside the function, use a loop to generate the specified number of users.
# For each user, create a dictionary with the keys name, address, and language_code.
# Use the faker instance to generate fake data for each key:
# name: faker.name()
# address: faker.address()
# language_code: faker.language_code()
# Append the user dictionary to the users list.
# Step 5: Call the function and print the users list

import faker
fake = faker.Faker()
users = []  

def add_user(users, number_of_users):
    for i in range(number_of_users):
        user = {
            'name': fake.name(),
            'address': fake.address(),
            'language_code': fake.language_code()
        }
        users.append(user)
    return users
    
print(add_user(users, 3))



# Exercise Gold

# Exercise 1 : Upcoming Holiday
# Instructions
# Write a function that displays today’s date.
# The function should also display the amount of time left from now until the next upcoming holiday and print which holiday that is. (Example: the next holiday is New Years’ Eve in 30 days).
# Hint: Use a module to find the datetime and name of the upcoming holiday.


import holidays
from datetime import date
def next_holiday(country):
    today = date.today()
    this_year = today.year
    
    holiday_dates = holidays.country_holidays(country, years=[this_year, this_year + 1])
    
    upcoming_holidays = []
    for holiday_date, name in holiday_dates.items():
        if holiday_date > today:
            upcoming_holidays.append((holiday_date, name))
    
    upcoming_holidays.sort()
    next_holiday = upcoming_holidays[0]
    
    diff = next_holiday[0] - today
    print(f"next holiday is {next_holiday[1]} in {diff.days} days")
    
    

next_holiday("IL")



# Exercise Ninja

# What you will learn
# Dunder Methods
# Classes/Objects


# Exercise 1 : Temperature
# Instructions
# Write a base class called Temperature.
# Implement the following subclasses: Celsius, Kelvin, Fahrenheit.
# Each of the subclasses should have a method which can convert the temperture to another type.
# You must consider different designs and pick the best one according to the SOLID Principle.
class Temperature:
    def __init__(self, degree):
        self.degree = degree

class Celsius(Temperature):
    def __init__(self, degree):
        super().__init__(degree)
        
    def convert_to_other(self, other):
        if other == 'Kelvin':
            return self.degree + 273.15
        if other == "Fahrenheit":
            return (self.degree * 9/5) + 32
        if other == "Celsius":
            return self.degree
        
        raise TypeError("Wrong type for conversion!") 
        
class Kelvin(Temperature):
    def __init__(self, degree):
        super().__init__(degree)
    
    def convert_to_other(self, other):
        if other == 'Celsius':
            return self.degree - 273.15
        if other == "Fahrenheit":
            return (self.degree - 273.15) * 9 / 5 + 32
        if other == 'Kelvin':
            return self.degree
        
        raise TypeError("Wrong type for conversion!") 


class Fahrenheit(Temperature):
    def __init__(self, degree,):
        super().__init__(degree)
    
    def convert_to_other(self, other):
        if other == 'Celsius':
            return (self.degree - 32) * 5 / 9
        if other == "Kelvin":
            return (self.degree - 32) * 5 / 9 + 273.15
        if other == 'Fahrenheit':
            return self.degree
        
        raise TypeError("Wrong type for conversion!") 

temp = Fahrenheit(32)
print(temp.convert_to_other('Celsius'))
print(temp.convert_to_other('Kelvin'))


