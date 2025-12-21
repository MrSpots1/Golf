import random

from CardSuit import CardSuit
from CardType import CardType
from CardClass import Card


class Deck:
    def __init__(
        self,
        deck_count: int,
    ):
        self.cards = []
        self.discards = []
        if deck_count < 1:
            raise ValueError("deck_count must be greater than 0")
        for i in range(deck_count):
            for suit in CardSuit:
                for type in CardType:
                    self.cards.append(Card(suit, type))

    def shuffle(self):
        if self.cards_left != 0:
            random.shuffle(self.cards)
        else:
            raise Exception("There are no cards in the draw pile to shuffle")

    def draw_card(self):
        if self.cards_left != 0:
            return self.cards.pop()
        else:
            raise IndexError("There are no cards left in the draw pile")

    def discard(self, card):
        self.discards.append(card)

    def topDiscardCard(self):
        if self.discards.__len__() == 0:
            raise Exception("There are no cards on the discard pile")
        return self.discards[-1]

    def cards_left(self):
        return self.cards.__len__()

    def discards_to_cards(self):
        if self.cards_left() == 0:
            self.cards = self.discards
            self.discards = []
            self.shuffle()
        else:
            raise Exception("There are still cards left in the draw pile")

