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
        
    def outOfCards(self):
        return not self.hand

class GoFishPlayer(Player):
    def giveAllCardsWithNumber(self, number):
        cardsToGive = [card for card in self.hand if card.number == number]
        for card in cardsToGive:
            self.hand.remove(card)
        return cardsToGive
    
    def gimmeTheFours(self):
        for card in self.hand:
            if len([x for x in self.hand if x.number == card.number]) == 4:
                return self.giveAllCardsWithNumber(card.number)
        return None
    
    def gimmeAllFours(self):
        allFours = []
        fours = self.gimmeTheFours()
        while (fours):
            allFours.append(fours)
            fours = self.gimmeTheFours()
        return allFours
            
class HumanGoFishPlayer(GoFishPlayer):
    def chooseCard(self):
        self.sortHand()
        print "Choose a card to ask about. You have: "
        self.printHand()
        num = 0
        while(not any(card.number == num for card in self.hand)):
            num = int(raw_input("Enter card number: "))
        return num
    
class RobotGoFishPlayer(GoFishPlayer):
    def chooseCard(self):
        max = [0,0]
        for card in self.hand:
            num = len([x for x in self.hand if x.number == card.number])
            if num > max[0]:
                max = [num, card.number]
        return max[1]
            
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
        self.graveyard = []
        self.deck = []
        self.players = []
    
    def createStandardShuffledDeck(self):
        d = Deck([2,3,4,5,6,7,8,9,10,J,Q,K,A],["Hearts","Clubs","Diamonds","Spades"])
        d.shuffleDeck()
        return d
    
class WarGame(Game):
    def __init__(self, players):
        self.deck = Game.createStandardShuffledDeck(self)
        self.players = players
    
    def dealCards(self):
        #Iterate through shuffled deck one card at a time and hand them to the players
        for num in range(self.deck.numCards()): #extra cards are dealt this way
            for player in self.players:
                if not self.deck.isEmpty():
                    player.addCard(self.deck.takeTopCard())
                else:
                    return
                    
    def isGameOver(self, playTilEnd):
        if playTilEnd and len(self.players) == 1:
            return True
        for player in self.players:
            if not player.hand:
                return True
        return False
    
    def runGame(self, shuffleAfterEveryRound, playTilEnd):
        print "Starting War Game!"
        print "Dealing cards"
        self.dealCards()
        print "Cards are dealt"
        print "Starting Game"
        roundNumber = 1
        while(not self.isGameOver(playTilEnd)):
            print "Starting Round ", roundNumber
            roundsCards = []
            for player in self.players:
                print player.name, " is starting his or her turn with ", len(player.hand), " cards."
                card = player.takeTurn()
                print player.name, " played a "
                card.printCard()
                roundsCards.append(card)
            winningPlayers = [0]
            winner = roundsCards[0]
            index = 0
            for i in range(1,len(roundsCards)):
                if roundsCards[i].number > winner.number:
                    index = i
                    winner = roundsCards[i]
                    winningPlayers = [i]
                elif roundsCards[i].number == winner.number:
                    winningPlayers.append(i)
            if len(winningPlayers)>1:
                stop = False
                print "Tie! The cards are shared."
                while not stop:
                    for index in winningPlayers:
                        if len(roundsCards) > 0:
                            self.players[index].addCard(roundsCards.pop())
                        else:
                            stop = True
                            break
            else:
                print "Player ", self.players[index].name, " won!"
                for card in roundsCards:
                    self.players[index].addCard(card)
            roundNumber+=1
            if shuffleAfterEveryRound:
                for player in self.players:
                    player.shuffleHand()
            if playTilEnd:
                for player in self.players:
                    if player.outOfCards():
                        print player.name, " has lost!"
                        self.players.remove(player)
        if playTilEnd:
            print self.players[0].name, " is the winner!"
        
class GoFishGame(Game):
    def __init__(self, players):
        self.deck = Game.createStandardShuffledDeck(self)
        self.players = players
    
    def dealCards(self):
        #Iterate through shuffled deck one card at a time and hand 5 to the players
        for num in range(5): #extra cards are dealt this way
            for player in self.players:
                if not self.deck.isEmpty():
                    player.addCard(self.deck.takeTopCard())
                else:
                    return
                
    def isGameOver(self, playTilEnd):
        if playTilEnd and len(self.players) == 1:
            return True
        for player in self.players:
            if not player.hand:
                return True
        return False
                
    def runGame(self, playTilEnd):
        print "Starting Go Fish!"
        print "Dealing cards"
        self.dealCards()
        print "Cards are dealt"
        print "Starting Game"
        #Add check for fours right before game starts
        while(not self.isGameOver(playTilEnd)):
            for player in self.players:
                won = True
                while won:
                    number = player.chooseCard()
                    #playerToAsk = player.choosePlayer(number)
                    if len(self.players) == 2:
                        playerToAsk = 0
                        if self.players[0] == player:
                            playerToAsk = 1
                        print player.name, " asked ", self.players[playerToAsk].name, " got any ", number, "'s?"
                        cards = self.players[playerToAsk].gotAny(number)
                        if cards:
                            print self.players[playerToAsk].name, ": Yup!"
                            for card in cards:
                                player.hand.append(card)
                                player.hand.sort()
                                #Check if we have four now
                        else:
                            print self.players[playerToAsk].name, ": Go Fish!"
                            won = False