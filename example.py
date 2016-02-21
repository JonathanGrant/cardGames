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
        self.points = 0
    
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
    def chooseCardAndPlayer(self, players):
        self.sortHand()
        print self.name, ", choose a card to ask about. You have: "
        self.printHand()
        num = 0
        while(not any(card.number == num for card in self.hand)):
            num = int(raw_input("Enter card number: "))
        print "Choose a player to ask. The players are: "
        for index in range(len(players)):
            print index, " ", players[index].name
        index = -1
        while(index < 0 or index >= len(players)):
            index = int(raw_input("Enter player number: "))
        return num, index
    
class PredictionCardForGoFish:
    #Player Score:
    #0 - Player definitely doesn't have the card
    #1 - Player might have the card
    #2 - Player definitely has at least 1 of this card
    #3 - Player definitely has at least 2 of this card
    #4 - Player definitely has at least 3 of this card
    def __init__(self, number, players):
        self.number = number
        self.players = players
        self.playerScores = []
        for num in (players):
            self.playerScores.append(1)
    
    def setPlayerScore(self, playerIndex, newScore):
        self.playerScores[playerIndex] = newScore
        
    def getPlayerScore(self, playerIndex):
        return self.playerScores[playerIndex]
    
    def getMaxPlayerScore(self, askingPlayerIndex):
        value = 0
        index = 0
        count = 0
        for score in self.playerScores:
            if value < score:
                if count != askingPlayerIndex:
                    value = score
                    index = count
            count += 1
        return index, value
    
class RobotGoFishPlayer(GoFishPlayer):
    predictionCards = []
    #Must be called once before playable AI
    @classmethod
    def createPredictionCards(cls, players):
        for num in range(2,A+1):
            cls.predictionCards.append(PredictionCardForGoFish(num, players))
    
    def __init__(self, name, hand, isEasy):
        self.name = name
        self.hand = hand
        self.isEasy = isEasy
        self.points = 0
        
    #This method will be called after every single turn
    @classmethod
    def cardWasAskedFor(cls, number, askingPlayerIndex, askedPlayerIndex, playerGaveCount):
        theCard = None
        for card in cls.predictionCards:
            if card.number == number:
                theCard = card
        if theCard:
            indexOfCard = cls.predictionCards.index(theCard)
            if cls.predictionCards[indexOfCard].getPlayerScore(askingPlayerIndex) <= 1:
                cls.predictionCards[indexOfCard].setPlayerScore(askingPlayerIndex, 2)
            if playerGaveCount > 0:
                cls.predictionCards[indexOfCard].setPlayerScore(askingPlayerIndex, playerGaveCount + cls.predictionCards[indexOfCard].getPlayerScore(askingPlayerIndex))
            cls.predictionCards[indexOfCard].setPlayerScore(askedPlayerIndex, 1)
        
    @classmethod
    def bookFinished(cls, number):
        toRemove = None
        for card in cls.predictionCards:
            if card.number == number:
                toRemove = card
        if toRemove:
            cls.predictionCards.remove(toRemove)
        
    def chooseCardAndPlayer(self, players):
        if self.isEasy:
            max = [0,0]
            for card in self.hand:
                num = len([x for x in self.hand if x.number == card.number])
                if num > max[0]:
                    max = [num, card.number]
            #Now randomly choose the person to ask
            playerNum = random.randint(0, len(players) - 1)
            while players[playerNum] == self:
                playerNum = random.randint(0, len(players) - 1)
            return max[1], playerNum
        else:
            #What is my player index?
            num = 0
            for num in range(0, len(players)):
                if self == players[num]:
                    break
            #Find max in predictionCards. if not me, return the number and player
            maxScore = [0, 0, 0]
            for number in self.predictionCards:
                #Only want to know if I have the card
                if len([x for x in self.hand if x.number == number.number]):
                    index, value = number.getMaxPlayerScore(num)
                    if maxScore[2] < value:
                        maxScore = [number.number, index, value]
            return maxScore[0], maxScore[1]
            
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
        self.books = []
    
    def dealCards(self):
        #Iterate through shuffled deck one card at a time and hand 5 to the players
        for num in range(5): #extra cards are dealt this way
            for player in self.players:
                if not self.deck.isEmpty():
                    player.addCard(self.deck.takeTopCard())
                else:
                    return
                
    #playTilEnd: Game is over when all but 1 players have no cards
    #else: Game is over when just 1 player has no cards
    def isGameOver(self, playTilEnd):
        for player in self.players:
            if not player.hand:
                #Give the player more cards
                if not playTilEnd:
                    return True
        if playTilEnd and len(self.players) == len(self.donePlayers):
            return True
        return False
    
    def checkAllPlayersForBooks(self):
        for player in self.players:
            fours = player.gimmeAllFours()
            if len(fours) > 0:
                self.books.append(fours) #it might not be append but the other command I can't remember right now
                player.points += len(fours)
                print player.name, "has", len(fours), "books, and has placed them down on the table."
                for four in fours:
                    RobotGoFishPlayer.bookFinished(four[0].number)

    def gameOver(self):
        print "Game Over!"
        #Print out the players names and their points in order
        self.players.sort(key=operator.attrgetter('points'), reverse=True)
        for player in range(0, len(self.players)):
            print player+1, " ", self.players[player].name, "has", self.players[player].points, "points"
                
    def outOfCardsCheck(self):
        for player in self.players:
            if player in self.donePlayers:
                pass
            if player.outOfCards():
                print player.name, "is out of cards!"
                if self.deck.isEmpty():
                    self.donePlayers.append(player)
                else:
                    #Give players up to five more cards
                    num = 0
                    for num in range(0,5):
                        if not self.deck.isEmpty():
                            newCard = self.deck.takeTopCard()
                            player.hand.append(newCard)
                        else:
                            break
                    print player.name, "picked up", num, "cards."
        if len(self.players) == len(self.donePlayers):
            self.gameOver()
                
    def runGame(self, playTilEnd):
        self.winners = []
        print "Starting Go Fish!"
        print "Dealing cards"
        self.dealCards()
        print "Cards are dealt"
        print "Starting Game"
        #Add check for fours right before game starts
        self.donePlayers = []
        RobotGoFishPlayer.createPredictionCards(self.players)
        while(not self.isGameOver(playTilEnd)):
            for player in self.players:
                #print self.donePlayers, " Done players"
                self.outOfCardsCheck()
                if player in self.donePlayers:
                    pass
                won = True
                while won and not self.isGameOver(playTilEnd):
                    if player in self.donePlayers:
                        break
                    number, playerToAsk = player.chooseCardAndPlayer(self.players)
                    print player.name, " asked ", self.players[playerToAsk].name, "got any ", number, "'s?"
                    cards = self.players[playerToAsk].giveAllCardsWithNumber(number)
                    RobotGoFishPlayer.cardWasAskedFor(number, self.players.index(player), playerToAsk, len(cards))
                    if cards:
                        print self.players[playerToAsk].name, ": Yup!"
                        print self.players[playerToAsk].name, "gave", player.name, len(cards), number, "'s"
                        for card in cards:
                            player.hand.append(card)
                            player.sortHand()
                            #Check if we have four now
                            self.checkAllPlayersForBooks()
                    else:
                        print self.players[playerToAsk].name, ": Go Fish!"
                        if not self.deck.isEmpty():
                            newCard = self.deck.takeTopCard()
                            player.hand.append(newCard)
                            print player.name, "picked up a", newCard.number, "of", newCard.suit
                            self.checkAllPlayersForBooks()
                        else:
                            print "But there are no cards left!"
                        won = False
                    self.outOfCardsCheck()
                if len(self.players) == len(self.donePlayers):
                    break
            if len(self.players) == len(self.donePlayers):
                break
        self.gameOver()

#Test!
#Create 2 human players only
playerOne = RobotGoFishPlayer("Skywalker", [], False)
playerTwo = HumanGoFishPlayer("Padme", [])
playerThree = HumanGoFishPlayer("Yoda", [])
playerFour = HumanGoFishPlayer("Rey", [])
game = GoFishGame([playerOne, playerTwo, playerThree, playerFour])
game.runGame(True)
#
#playerOne = WarPlayer("Skywalker", [])
#playerTwo = WarPlayer("Kenobi", [])
#playerThree = WarPlayer("Padme", [])
#playerFour = WarPlayer("Rey", [])
#game = WarGame([playerOne,playerTwo,playerThree, playerFour])
#game.runGame(True, True)