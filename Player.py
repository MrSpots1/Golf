from GameState import GameState
from GolfHand import GolfHand
from PlayerType import PlayerType 
from Card import Card

from TurnResult import TurnResult

class Player:
    def __init__(self, name: str, playerType: PlayerType, playerIndex: int):
        self.name = name
        self.playerType = playerType
        self.playerIndex = playerIndex
        self.hand = GolfHand()

    def display(self):
        print(f"Player: {self.name} [{self.playerType.name}")
        self.hand.display()

    def playTurn(self, gameState: GameState) -> TurnResult:
        pass  # No implementation here — must be overridden

    def watchTurn(self, originalState: GameState, playerIndex: int, turnResult: TurnResult) -> None:
        return # No implementation for default implementation