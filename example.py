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
    
    def isEmpty(self):
        return (not self.cards)
    
    def numCards(self):
        return len(self.cards)

class Player:
    def __init__(self, name, hand):
        self.hand = hand
        self.name = name
    
    def printName(self):
        print self.name
    
    def printHand(self):
        for card in self.hand:
            card.printCard()
            
    def sortHand(self):
        self.hand.sort(key=operator.attrgetter('number'))
        
    def addCard(self, newCard):
        self.hand.insert(0, newCard)
        
    def shuffleHand(self):
        random.shuffle(self.hand)
            
class WarPlayer(Player):
    def playCard(self):
        #returns the top card
        return self.hand.pop()
    
    def takeTurn(self):
        return self.playCard()

class HumanWarPlayer(WarPlayer):
    def takeTurn(self):
        raw_input("Press Enter to make turn")
        return self.playCard()
    
class Game:
    def __init__(self):
        print "Game Created"
    
    def createStandardShuffledDeck(self):
        d = Deck([2,3,4,5,6,7,8,9,10,J,Q,K,A],["Hearts","Clubs","Diamonds","Spades"])
        d.shuffleDeck()
        return d
    
class WarGame(Game):
    def __init__(self, players):
        self.deck = Game.createStandardShuffledDeck(self)
        self.players = players
        self.graveyard = []
    
    def dealCards(self):
        #Iterate through shuffled deck one card at a time and hand them to the players
        for num in range(self.deck.numCards() / len(self.players)): #extra cards are dealt this way
            for player in self.players:
                if not self.deck.isEmpty():
                    player.addCard(self.deck.takeTopCard())
                    
    def isGameOver(self):
        for player in self.players:
            if not player.hand:
                return True
        return False
    
    def runGame(self, shuffleAfterEveryRound):
        print "Starting War Game!"
        print "Dealing cards"
        self.dealCards()
        print "Cards are dealt"
        print "Starting Game"
        roundNumber = 1
        while(not self.isGameOver()):
            print "Starting Round ", roundNumber
            roundsCards = []
            for player in self.players:
                print player.name, " is starting his or her turn with ", len(player.hand), " cards."
                card = player.takeTurn()
                print player.name, " played a "
                card.printCard()
                roundsCards.append(card)
            isTie = False
            winner = roundsCards[0]
            index = 0
            for i in range(1,len(roundsCards)):
                if roundsCards[i] > winner:
                    index = i
                    winner = roundsCards[i]
                    isTie = False
                elif roundsCards[i] == winner:
                    isTie = True
            if isTie:
                print "Tie! The cards are deleted."
                for card in roundsCards:
                    self.graveyard.append(card)
            else:
                print "Player ", self.players[index].name, " won!"
                for card in roundsCards:
                    self.players[index].addCard(card)
            roundNumber+=1
            if shuffleAfterEveryRound:
                for player in self.players:
                    player.shuffleHand()
        
playerOne = HumanWarPlayer("Jonathan",[])
playerTwo = WarPlayer("Count Dooku",[])
w = WarGame([playerOne, playerTwo])
w.runGame(True)