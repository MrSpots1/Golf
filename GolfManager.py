from CardSuit import CardSuit
from CardType import CardType
from Card import Card
from CardDeck import CardDeck

class GolfManager:
    def __init__(self):
        self.deck = CardDeck(2)
        self.deck.shuffle()

