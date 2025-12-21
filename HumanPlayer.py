from GameState import GameState
from Player import Player
from PlayerType import PlayerType
from TurnResult import TurnResult

class HumanPlayer(Player):
    def __init__(self, name: str, playerIndex: int):
        super().__init__(name, PlayerType.Human, playerIndex)

    def playTurn(self, gameState: GameState) -> TurnResult:
        return TurnResult()  # Implementation for human player turn

    def watchTurn(self, originalState: GameState, playerIndex: int, turnResult: TurnResult) -> None:
        pass # No implementation for default implementation