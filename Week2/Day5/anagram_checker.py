
class AnagramChecker:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            words = [line.strip().lower() for line in file]
            self.words = words
            
    def is_valid_word(self, word):
        return word in self.words
    
    def is_anagram(self, word1, word2):
        return sorted(word1) == sorted(word2)
    
    def get_anagrams(self, word):
        anagrams = []
        for value in self.words:
            if self.is_anagram(word, value) and value not in anagrams:
                anagrams.append(value)
        
        return anagrams
