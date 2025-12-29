from CardSlot import CardSlot
from GameState import GameState
from GolfHand import GolfHand
from PlayerType import PlayerType 
from Card import Card

from TurnResult import TurnResult

class Player:
    def __init__(self, name: str, playerType: PlayerType):
        self.name = name
        self.playerType = playerType

    def initializeHand(self):
        self.hand = GolfHand()

    def initialReveal(self) -> None:
        pass  # No implementation here — must be overridden for the player to reveal two cards

    def observeGameState(self, gameState: GameState) -> None:
        pass  # No implementation for default implementation

    def considerDiscardCard(self, gameState: GameState, card: Card) -> CardSlot | None:
        return False  # Default implementation does not consider the discard card
    
    def considerDrawCard(self, gameState: GameState, card: Card) -> CardSlot | None:
        return False  # Default implementation does not consider the draw card
    
    def watchDiscard(self, gameState: GameState, slot: CardSlot | None, slotIsFacedown: bool, discardCard: Card | None, newDiscard: Card | None) -> None:
        # slot, discardCard, and newDiscard are all None if the discard card was not taken
        # all have vaues if it is taken
        return # No implementation for default implementation
    
    def watchDraw(self, gameState: GameState, slot: CardSlot | None, slotIsFacedown: bool, drawnCard: Card, newDiscard: Card) -> None:
        # slot is None if the drawn card was discarded
        return # No implementation for default implementation
    