from GameState import GameState
import Player
from PlayerType import PlayerType
import TurnResult


class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name, PlayerType.Human)

    def playTurn(self, gameState: GameState) -> TurnResult:
        pass  # No implementation here — must be overridden

    def watchTurn(self, originalState: GameState, playerIndex: int, turnResult: TurnResult) -> None:
        return # No implementation for default implementation