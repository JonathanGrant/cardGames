def Card:
    cardCount = 0
    
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        Card.cardCount+=1
        
def Deck:
    def __init__(self, cards, suits):
        self.cards = cards
        self.suits = suits
        #Now we create the cards and put it into the deck
        self.cards = []
        for i in cards:
            for j in suits:
                self.cards.append(new Card(i,j))
        #Now shuffle deck!