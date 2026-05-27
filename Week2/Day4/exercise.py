import random
import requests
#  Exercise 1: Random Sentence Generator
# Goal: Create a program that generates a random sentence of a specified length from a word list.

# Key Python Topics:

# File handling (open(), read())
# Lists
# Random number generation (random.choice())
# String manipulation (split(), join(), lower())
# Error handling (try, except)
# Input validation

# Instructions:

# Download the provided word list and save it in your development directory.
# Create a function to read the words from the file.
# Create a function to generate a random sentence of a given length.
# Create a main function to handle user input and program flow.

# Step 1: Create the get_words_from_file function
# Create a function named get_words_from_file that takes the file path as an argument.
# Open the file in read mode ("r").
# Read the file content.
# Split the content into a list of words.
# Return the list of words.

def get_words_from_file():
    words = []
    try:
        with open('words.txt', 'r') as file:
            words = [line.strip() for line in file]
    except Exception as error:
        print(f'Something went wrong! {error}')
    return words

# Step 2: Create the get_random_sentence function
# Create a function named get_random_sentence that takes the sentence length as an argument.
# Call get_words_from_file to get the list of words.
# Select a random word from the list length times.
# Create a sentence with the selected words.
# Convert the sentence to lowercase.
# Return the sentence.
def get_random_sentence(length):
    random_words = []
    words = get_words_from_file()
    for i in range(length):
        word = random.choice(words)
        random_words.append(word)
    
    return (" ".join(random_words).lower() + '.')

# print(get_random_sentence(10))
        
# Step 3: Create the main function
# Create a function named main.
# Print a message explaining the program’s purpose.
# Ask the user for the desired sentence length.
# Validate the user input:
# Check if it is an integer.
# Check if it is between 2 and 20 (inclusive).
# If the input is invalid, print an error message and exit.
# If the input is valid, call get_random_sentence with the length and print the generated sentence.

def main():
    print("This program will generate a sentence with specified length.")
    
    try:
        length = int(input("Please specify the length of the sentence (2-20): "))
    except TypeError:
        print('Invalid input! Please input an integer between 2 and 20')
        return
    
    if length < 2 or length > 20:
        print('Invalid Input! Length should be between 2 and 20.')
        return
    
    print(get_random_sentence(length))
    return

# main()    
    


# 🌟 Exercise 2: Working with JSON
# Goal: Access a nested key in a JSON string, add a new key, and save the modified JSON to a file.

# Key Python Topics:

# JSON parsing (json.loads())
# JSON serialization (json.dump())
# Dictionaries
# File handling (open())

# Instructions:

# Using the follow code:

import json
sampleJson = """{ 
    "company":{ 
        "employee":{ 
            "name":"emma",
            "payable":{ 
                "salary":7000,
                "bonus":800
            }
        }
    }
}"""




# Access the nested “salary” key.
# Add a new key “birth_date” wich value is of format “YYYY-MM-DD”, to the “employee” dictionary: "birth_date": "YYYY-MM-DD".
# Save the modified JSON to a file.


# Step 1: Load the JSON string

# Import the json module.
# Use json.loads() to parse the JSON string into a Python dictionary.

sampleDict = json.loads(sampleJson)
print(sampleDict)

# Step 2: Access the nested “salary” key

# Access the “salary” key using nested dictionary access (e.g., data["company"]["employee"]["payable"]["salary"]).
# Print the value of the “salary” key.
print(sampleDict["company"]["employee"]["payable"]["salary"])

# Step 3: Add the “birth_date” key

# Add a new key-value pair to the “employee” dictionary: "birth_date": "YYYY-MM-DD".
# Replace "YYYY-MM-DD" with an actual date.
sampleDict["company"]["employee"]["birth_date"] = "1999-02-02"

# Step 4: Save the JSON to a file

# Open a file in write mode ("w").
# Use json.dump() to write the modified dictionary to the file in JSON format.
# Use the indent parameter to make the JSON file more readable.
with open('file.json', 'w') as file:
    json.dump(sampleDict, file, indent=2, sort_keys=True)

# exercise Gold

# Exercise 2 : Giphy API #1
# Instruction
# Hint: For this exercise, check out the documentation of the Giphy API

# You will work with this part of the documention

# You will use this Gif URL: https://api.giphy.com/v1/gifs/search?q=hilarious&rating=g&api_key=hpvZycW22qCjn5cRM1xtWB8NKq4dQ2My
# Explanation of the Gif URL

# q Request Paramater: Search query term or phrase. We are searching for “hilarious” gifs
# rating Request Paramater: Filters results by specified rating. We are searching for Level 1 gifs. Check out the ratings documentation

# api_key Request Paramater : GIPHY API Key. Our API KEY is hpvZycW22qCjn5cRM1xtWB8NKq4dQ2My
# Fetch the giphs from the Gif URL provided above.
# Use f-strings and variables to build the URL string we’re using for the fetch.
# If the status code is 200 return the result as a JSON object.
# Only return gifs which have a height bigger then 100.
# Return the length of the object you received in the previous question.
# Only return the first 10 gifs. Hint: In the Giphy Documentation, check out the relevant Request Parameters.
params = {
    "q": "hilarious",
    "rating": "g",
    "api_key": "hpvZycW22qCjn5cRM1xtWB8NKq4dQ2My",
    # "limit": 10
    }

def get_gifs(params):
    url = "https://api.giphy.com/v1/gifs/search"
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Request failed!")
        return []
    data = response.json()['data']
    gifs = [gif for gif in data if int(gif['images']['fixed_height']['height']) > 100]        
    return gifs[:10]

print(len(get_gifs(params=params)))
    