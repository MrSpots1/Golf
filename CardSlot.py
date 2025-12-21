from CardSuit import CardSuit
from CardType import CardType
from CardClass import Card

class CardSlot:
    def __init__(
        self
    ):
        self.card = None
        self.isFaceDown = True

    def placeHiddenCard(self, card: Card):
        if (self.card is not None):
            raise ValueError("CardSlot already has a card.")
        self.card = card
        self.isFaceDown = True

    def revealCard(self):
        if(self.isFaceDown == False):
            raise ValueError("Card is already revealed.")
        self.isFaceDown = False
    
    def placeRevealedCard(self, card: Card):
        self.card = card
        self.isFaceDown = False

    def display(self) -> str:
        if self.isFaceDown:
            return "??"
        else:
            return self.card.display()