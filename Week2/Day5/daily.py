import random
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

class Deck:
    suits = ['Heart', 'Diamond', 'Club', 'Spade']
    values = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    def __init__(self):
        self.cards = []
        for suit in Deck.suits:
            for value in Deck.values:
                self.cards.append((suit, value))
    
    def shuffle(self):
        random.shuffle(self.cards)
        return self.cards
    
    def deal(self):
        dealt = self.cards.pop()
        return dealt
        
d1 = Deck()
d1.shuffle()

print(d1.cards)

print(d1.deal())
print(d1.deal())
print(d1.deal())
print(d1.deal())
print(d1.deal())
print(d1.cards)
