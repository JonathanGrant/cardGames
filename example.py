import random

class Card:
    cardCount = 0
    
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        Card.cardCount+=1
    
    def printCard(self):
        if self.number > 10:
            print("%i of %s."%{self.number, self.suit})
        else:
            print("%i of %s."%{self.number, self.suit})
        
class Deck:
    def __init__(self, cardList, suitList):
        self.cardList = cardList
        self.suitList = suitList
        #Now we create the cards and put it into the deck
        self.cards = []
        for i in cardList:
            for j in suitList:
                self.cards.append(Card(i,j))
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def printDeck(self):
        for card in self.cards:
            card.printCard()