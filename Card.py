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

    def str(self) -> str:
        type_map = {
            CardType.Ace: "A",
            CardType.Jack: "J",
            CardType.Queen: "Q",
            CardType.King: "K",
        }

        suit_map = {
            CardSuit.Spade: "♠",
            CardSuit.Heart: "♥",
            CardSuit.Diamond: "♦",
            CardSuit.Club: "♣",
        }

        rank = type_map.get(self.type, str(self.type.value))
        suit = suit_map[self.suit]

        return f"{rank}{suit}"