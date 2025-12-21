from CardSuit import CardSuit
from CardType import CardType
from CardClass import Card
from PlayerType import GameModes
from CardDeck import Deck

class GolfManager:
    def __init__(self):
        self.deck = Deck(2)
        self.deck.shuffle()


