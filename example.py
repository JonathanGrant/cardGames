import random

J = 11
Q = 12
K = 13

class Card:
    cardCount = 0
    
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        Card.cardCount+=1
    
    def printCard(self):
        if self.number > 10:
            print self.number, " of ", self.suit
        else:
            print self.number, " of ", self.suit
        
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

print "Creating Deck"
myDeck = Deck([2,3,4,5,6,7,8,9,10,J,Q,K],["Spades","Diamonds","Hearts","Clubs"])
myDeck.printDeck()
myDeck.shuffle()
myDeck.printDeck()