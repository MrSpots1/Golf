from CardDeck import CardDeck
from Card import Card
from enum import Enum
from GameState import GameState

class TurnAction(Enum):
    TookFromDiscardPile = 1
    TookFromDrawPile = 2
    DiscardedDrawnCard = 3

class TurnResult:
    def __init__(self, newState: GameState, action: TurnAction, takenCard: Card, playedAtRow: int, playedAtColumn: int, discard: Card):
        self.newState = newState
        self.action = action
        self.takenCard = takenCard
        self.playedAtRow = playedAtRow
        self.playedAtColumn = playedAtColumn
        self.discard = discard

    def describe(self) -> str:
        description = ""
        if self.action == TurnAction.TookFromDiscardPile:
            description = f"Took the {self.takenCard.str()} from the discard card pile and played it at ({self.playedAtRow+1}, {self.playedAtColumn+1}), replacing a {self.discard.str()}"
        elif self.action == TurnAction.TookFromDrawPile:
            description = f"Drew a {self.takenCard.str()} from the draw pile and played it at ({self.playedAtRow+1}, {self.playedAtColumn+1}), replacing a {self.discard.str()}"
        else:
            description = f"Drew a {self.discard.str()} from the draw pile and discarded it."
        return description
