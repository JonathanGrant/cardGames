import operator
import random

J = 11
Q = 12
K = 13
A = 14

class Card:
    cardCount = 0
    
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        Card.cardCount+=1
    
    def printCard(self):
        if self.number > 10:
            if self.number == J:
                print "Jack of ", self.suit
            elif self.number == Q:
                print "Queen of ", self.suit
            elif self.number == K:
                print "King of ", self.suit
            elif self.number == A:
                print "Ace of ", self.suit
            else:
                print "Card number not understood. ", self.number
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
    
    def shuffleDeck(self):
        random.shuffle(self.cards)
        
    def printDeck(self):
        for card in self.cards:
            card.printCard()
    
    def peakTopCard(self):
        self.cards[-1].printCard()
        
    def takeTopCard(self):
        return self.cards.pop()

class Player:
    def __init__(self, hand):
        self.hand = hand
    
    def printHand(self):
        for card in self.hand:
            card.printCard()
            
    def sortHand(self):
        self.hand.sort(key=operator.attrgetter('number'))
        
    def addCards(self, newCards):
        for card in newCards:
            self.hand.append(card)
            
class WarPlayer(Player):
    def playCard(self):
        #returns the top card
        return self.hand.pop()
    
class Game:
    def __init__(self):
        print "Game Created"
    
    def createStandardShuffledDeck(self):
        d = Deck([2,3,4,5,6,7,8,9,10,J,Q,K,A],["Hearts","Clubs","Diamonds","Spades"])
        d.shuffleDeck()
        return d
    
class WarGame(Game):
    def __init__(self):
        self.deck = Game.createStandardShuffledDeck(self)

print WarGame().deck