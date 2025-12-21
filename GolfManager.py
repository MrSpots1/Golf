from CardSuit import CardSuit
from CardType import CardType
from CardClass import Card
from GameModes import GameModes
from CardDeck import Deck

class GolfManager:
    def __init__(self, mode):
        if mode < 0 or mode > 4:
            raise ValueError("Invalid mode")
        self.mode = GameModes(mode)
        self.deck = Deck(2)
        self.deck.shuffle()
        self.player_one_hand = []
        self.player_two_hand = []
        for i in range(6):
            self.player_one_hand.append(self.deck.draw_card())
            self.player_two_hand.append(self.deck.draw_card())

