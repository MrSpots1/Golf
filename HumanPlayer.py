from GameState import GameState
from Player import Player
from PlayerType import PlayerType
from TurnResult import TurnResult

class HumanPlayer(Player):
    def __init__(self, name: str, playerIndex: int):
        super().__init__(name, PlayerType.Human, playerIndex)

    def initialReveal(self) -> None:
        pos_row = input(f"Player {self.name}, what row you would like to reveal first? (1 or 2): ")
        while True:
            if pos_row == "1" or pos_row == "2":
                break
            pos_row = input("Invalid option, please try again: ")
        pos_row = int(pos_row) - 1
        pos_col = input(f"Player {self.name}, what column you would like to reveal first? (1-3): ")
        while True:
            if pos_col == "1" or pos_col == "2" or pos_col == "3":
                break
            pos_col = input("Invalid option, please try again: ")
        pos_col = int(pos_col) - 1
        self.hand.revealCard(pos_row, pos_col)

        pos_row = input(f"Player {self.name}, what row you would like to reveal second? (1 or 2): ")
        while True:
            if pos_row == "1" or pos_row == "2":
                break
            pos_row = input("Invalid option, please try again: ")
        pos_row = int(pos_row) - 1
        pos_col = input(f"Player {self.name}, what column you would like to reveal second? (1-3): ")
        while True:
            if pos_col == "1" or pos_col == "2" or pos_col == "3":
                break
            pos_col = input("Invalid option, please try again: ")
        pos_col = int(pos_col) - 1
        self.hand.revealCard(pos_row, pos_col)

    def playTurn(self, gameState: GameState) -> TurnResult:
        option = input("Do you want to take the top card of the discard pile, or the top card of the draw pile? (1 = discard pile, 2 = draw pile): ")
        tookDiscard = False
        while True:
            if option == "1" or option == "2":
                break
            option = input("Invalid option, please try again: ")
        card = None
        if option == "1":
            card = gameState.cardDeck.topDiscardCard()
            tookDiscard = True
        elif option == "2":
            card = gameState.cardDeck.draw_card()
            answer = input("Do you want to take this card or discard it? (1 = take, 2 = discard)")
            while True:
                if answer == "1" or answer == "2":
                    break
                answer = input("Invalid option, please try again: ")
            if answer == "2":
                gameState.cardDeck.discard(card)
                return TurnResult(gameState, False, card, False, -1, -1, card)
        pos_row = input("What row you would like to place your card? (1 or 2): ")
        while True:
            if pos_row == "1" or pos_row == "2":
                break
            pos_row = input("Invalid option, please try again: ")
        pos_row = int(pos_row) - 1
        pos_col = input("What column you would like to place your card? (1-3): ")
        while True:
            if pos_col == "1" or pos_col == "2" or pos_col == "3":
                break
            pos_col = input("Invalid option, please try again: ")
        pos_col = int(pos_col) - 1
        old_card = gameState.players[gameState.playerIndex].hand.getSlot(pos_row, pos_col).card
        gameState.cardDeck.discard(old_card)
        gameState.players[gameState.playerIndex].hand.placeRevealedCard(pos_row, pos_col, card)
        return TurnResult(gameState, tookDiscard, card, False, pos_row, pos_col, old_card)  # Implementation for human player turn

    def watchTurn(self, originalState: GameState, playerIndex: int, turnResult: TurnResult) -> None:
        pass # No implementation for default implementation