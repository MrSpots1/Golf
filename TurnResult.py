from CardDeck import CardDeck
from Card import Card
from GameState import GameState

class TurnResult:
    def __init__(self, originalState: GameState, tookDiscard: bool, drawnCard: Card, tookDrawnCard: bool, playedAtRow: int, playedAtColumn: int, discard: Card):
        self.originalState = originalState
        self.tookDiscard = tookDiscard
        self.drawnCard = drawnCard
        self.tookDrawnCard = tookDrawnCard
        self.playedAtRow = playedAtRow
        self.playedAtColumn = playedAtColumn
        self.discard = discard

    def describe(self) -> str:
        description = ""
        if self.tookDiscard:
            description += f"Took the discard card: {self.drawnCard.display()}\n"
        else:
            description += f"Drew a new card: {self.drawnCard.display()}\n"

        if self.playedAtColumn != -1 and self.playedAtRow != -1:
            description += f"Played the drawn card at position ({self.playedAtRow}, {self.playedAtColumn})\n"
        else:
            description += f"Discarded the drawn card: {self.drawnCard.display()}\n"

        return description
