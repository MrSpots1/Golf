from CardDeck import CardDeck
from Card import Card
from GameState import GameState

class TurnResult:
    def __init__(self, newState: GameState, tookDiscard: bool, drawnCard: Card, tookDrawnCard: bool, playedAtRow: int, playedAtColumn: int, discard: Card):
        self.newState = newState
        self.tookDiscard = tookDiscard
        self.drawnCard = drawnCard
        self.tookDrawnCard = tookDrawnCard
        self.playedAtRow = playedAtRow
        self.playedAtColumn = playedAtColumn
        self.discard = discard
