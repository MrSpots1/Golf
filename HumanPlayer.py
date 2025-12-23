from GameState import GameState
from Player import Player
from PlayerType import PlayerType
from TurnResult import TurnResult


def input_checker(initial_message, acceptable_values):
    initial_answer = input(initial_message)
    while True:
        if initial_answer in acceptable_values:
            return initial_answer
        initial_answer = input("Invalid option, please try again: ")


class HumanPlayer(Player):
    def __init__(self, name: str, playerIndex: int):
        super().__init__(name, PlayerType.Human, playerIndex)

    def initialReveal(self) -> None:
        pos_row = int(input_checker(f"Player {self.name}, what row you would like to reveal first? (1 or 2): ", ["1", "2"])) - 1
        pos_col = int(input_checker(f"Player {self.name}, what column you would like to reveal first? (1-3): ", ["1", "2", "3"])) - 1
        self.hand.revealCard(pos_row, pos_col)

        while True:
            pos_row2 = int(input_checker(f"Player {self.name}, what row you would like to reveal for the second card? (1 or 2): ", ["1", "2"])) - 1
            pos_col2 = int(input_checker(f"Player {self.name}, what column you would like to reveal for the second card? (1-3): ",["1", "2", "3"])) - 1
            if pos_row2 == pos_row and pos_col2 == pos_col:
                print("That is the same position as your first card, please try again. ")
            else:
                break
        self.hand.revealCard(pos_row2, pos_col2)

    def playTurn(self, gameState: GameState) -> TurnResult:
        option = input_checker("Do you want to take the top card of the discard pile, or the top card of the draw pile? (1 = discard pile, 2 = draw pile): ",["1", "2"])
        tookDiscard = False
        card = None
        if option == "1":
            card = gameState.cardDeck.topDiscardCard()
            tookDiscard = True
        elif option == "2":
            card = gameState.cardDeck.draw_card()
            print(f"You got the card: {card.display()}")
            answer = input_checker("Do you want to take this card or discard it? (1 = take, 2 = discard): ",["1", "2"])
            if answer == "2":
                gameState.cardDeck.discard(card)
                return TurnResult(gameState, False, card, False, -1, -1, card)
        pos_row = int(
            input_checker(f"What row you would like to place your card? (1 or 2): ",
                          ["1", "2"])) - 1
        pos_col = int(
            input_checker(f"What column you would like to place your card? (1-3): ",
                          ["1", "2", "3"])) - 1

        old_card = gameState.players[gameState.playerIndex].hand.getSlot(pos_row, pos_col).card
        gameState.cardDeck.discard(old_card)
        gameState.players[gameState.playerIndex].hand.placeRevealedCard(pos_row, pos_col, card)
        return TurnResult(gameState, tookDiscard, card, False, pos_row, pos_col, old_card)  # Implementation for human player turn

    def watchTurn(self, originalState: GameState, playerIndex: int, turnResult: TurnResult) -> None:
        pass # No implementation for default implementation