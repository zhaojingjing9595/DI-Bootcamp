import json
import random
import re
import string
# Instructions:

# Create a Text class to analyze text data, either from a string or a file. Then, create a TextModification class to perform text cleaning.



# Part I: Analyzing a Simple String

# Step 1: Create the Text Class

# Create a class called Text.
# The __init__ method should take a string as an argument and store it in an attribute (e.g: self.text).
class Text:
    def __init__(self, text_str):
        self.text = text_str
    
    # Step 2: Implement word_frequency Method
    # Create a method called word_frequency(word).
    # Split the text attribute into a list of words.
    # Count the occurrences of the given word in the list.
    # Return the count.
    # If the word is not found, return None or a meaningful message.

    def word_frequency(self, word):
        words = self.text.split()
        count = words.count(word)
        if count > 0:
            return count
        return None

    # Step 3: Implement most_common_word Method

    # Create a method called most_common_word().
    # Split the text into a list of words.
    # Use a dictionary to store word frequencies.
    # Find the word with the highest frequency.
    # Return the most common word.
    def get_words_count(self):
        words = self.text.split()
        words_count = {}
        for word in words:
            if word in words_count:
                words_count[word] += 1
            else:
                words_count[word] = 1
        
        return words_count
        
    
    def most_common_word(self):
        words_count = self.get_words_count()
        most_common = ""
        highest_count = 0

        for word, count in words_count.items():
            if count > highest_count:
                highest_count = count
                most_common = word

        return most_common
            
    # Step 4: Implement unique_words Method

    # Create a method called unique_words().
    # Split the text into a list of words.
    # Use a set to store unique words.
    # Return the unique words as a list.
    
    def unique_words(self):
        words = self.text.split()
        return list(set(words))
        
    # Part II: Analyzing Text from a File

    # Step 5: Implement from_file Class Method

    # Create a class method called from_file(file_path).
    # Open the file at file_path in read mode.
    # Read the file content.
    # Create and return a Text instance with the file content as the text.
    def from_file(self, file_path):
        with open(file_path, 'r') as file:
            text = json.load(file)
        return Text(text)

# Bonus: Text Modification

# Step 6: Create the TextModification Class

# Create a class called TextModification that inherits from Text.
class TextModification(Text):
    def __init__(self, text_str):
        super().__init__(text_str)
    

    # Step 7: Implement remove_punctuation Method

    # Create a method called remove_punctuation().
    # Use the string module to get a string of punctuation characters.
    # Use a string method or regular expressions to remove punctuation from the text attribute.
    # Return the modified text.
    def remove_punctuation(self):
        clean_text = ""

        for char in self.text:
            if char not in string.punctuation:
                clean_text += char

        return clean_text
        


    # Step 8: Implement remove_stop_words Method

    # Create a method called remove_stop_words().
    # Search online for a list of English stop words (common words like “a”, “the”, “is”).
    # Split the text into a list of words.
    # Filter out stop words from the list.
    # Join the remaining words back into a string.
    # Return the modified text.
    def remove_stop_words(self):
        stop_words = {
            "a", "an", "the",
            "is", "are", "am", "was", "were",
            "in", "on", "at", "to", "for", "from",
            "and", "or", "but",
            "of", "with", "as",
            "this", "that", "these", "those",
            "it", "he", "she", "they", "we", "you", "i"
        }

        words = self.text.split()
        filtered_words = [ word for word in words if word.lower() not in stop_words ]
        return " ".join(filtered_words)
        


    # Step 9: Implement remove_special_characters Method

    # Create a method called remove_special_characters().
    # Use regular expressions to remove special characters from the text attribute.
    # Return the modified text.
    def remove_special_characters(self):
        clean_text = re.sub(r"[^a-zA-Z0-9\s]", "", self.text)
        return clean_text


text = "i and the Lorem ipsum dolor dolor sit! amet32!, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
t1 = Text(text)
print(t1.text)
print(t1.get_words_count())
print(t1.most_common_word())
print(t1.unique_words())
print(t1.word_frequency('et'))
t2 = TextModification(text)
print(t2.remove_punctuation())
print(t2.remove_stop_words())

        