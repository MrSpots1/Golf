from CardSuit import CardSuit
from CardType import CardType

class Card:
    def __init__(
        self,
        card_suit: CardSuit,
        card_type: CardType
    ):
        self.suit = card_suit
        self.type = card_type
