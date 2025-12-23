from CardDeck import CardDeck
from Card import Card
from GameState import GameState

class TurnResult:
    def __init__(self, newState: GameState, tookDiscard: bool, takenCard: Card, tookDrawnCard: bool, playedAtRow: int, playedAtColumn: int, discard: Card):
        self.newState = newState
        self.tookDiscard = tookDiscard
        self.takenCard = takenCard
        self.tookDrawnCard = tookDrawnCard
        self.playedAtRow = playedAtRow
        self.playedAtColumn = playedAtColumn
        self.discard = discard

    def describe(self) -> str:
        description = ""
        if self.tookDiscard:
            description += f"Took the discard card: {self.takenCard.display()}\n"
        else:
            description += f"Drew a new card: {self.takenCard.display()}\n"

        if self.playedAtColumn != -1 and self.playedAtRow != -1:
            description += f"Played the drawn card at position ({self.playedAtRow}, {self.playedAtColumn})\n"
        else:
            description += f"Discarded the drawn card: {self.takenCard.display()}\n"

        return description
