from Card import Card
from CardSlot import CardPosition, CardSlot
from GameState import GameState
from Player import Player
from PlayerType import PlayerType
from TurnResult import TurnAction, TurnResult


def input_checker(initial_message, acceptable_values):
    initial_answer = input(initial_message)
    while True:
        if initial_answer in acceptable_values:
            return initial_answer
        initial_answer = input("Invalid option, please try again: ")


class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name, PlayerType.Human)

    def initialReveal(self) -> None:
        pos_row = int(input_checker(f"Player {self.name}, what row you would like to reveal first? (1 or 2): ", ["1", "2"])) - 1
        pos_col = int(input_checker(f"Player {self.name}, what column you would like to reveal first? (1, 2, or 3): ", ["1", "2", "3"])) - 1
        self.hand.revealCard(CardPosition(pos_row, pos_col))

        while True:
            pos_row2 = int(input_checker(f"Player {self.name}, what row you would like to reveal for the second card? (1 or 2): ", ["1", "2"])) - 1
            pos_col2 = int(input_checker(f"Player {self.name}, what column you would like to reveal for the second card? (1, 2, or 3): ",["1", "2", "3"])) - 1
            if pos_row2 == pos_row and pos_col2 == pos_col:
                print("That is the same position as your first card, please try again. ")
            else:
                break
        self.hand.revealCard(CardPosition(pos_row2, pos_col2))

    def considerDiscardCard(self, gameState: GameState, card: Card) -> CardSlot | None:
        option = input_checker(f"Do you want to take the {card.str()}, or draw? (1 = take {card.str()}, 2 = draw): ",["1", "2"])
        if option == "1":
            return self.hand.getSlot(self.__inputPosition())
        return None 
    
    def considerDrawCard(self, gameState: GameState, card: Card) -> CardSlot | None:
        option = input_checker(f"Do you want to take drawn {card.str()}? (1 = take {card.str()}, 2 = discard): ",["1", "2"])
        if option == "1":
            return self.hand.getSlot(self.__inputPosition())    
        return None  # Default implementation does not consider the draw card

    def __inputPosition(self) -> CardPosition:
        pos_row = int(
            input_checker(f"What row you would like to place your card? (1 or 2): ",
                          ["1", "2"])) - 1
        pos_col = int(
            input_checker(f"What column you would like to place your card? (1, 2, or 3): ",
                          ["1", "2", "3"])) - 1
        return CardPosition(pos_row, pos_col)

    def watchDiscard(self, gameState: GameState, slot: CardSlot | None, slotIsFacedown: bool, discardCard: Card | None, newDiscard: Card | None) -> None:
        # slot, discardCard, and newDiscard are all None if the discard card was not taken
        # all have vaues if it is taken
        return # No implementation for default implementation
    
    def watchDraw(self, gameState: GameState, slot: CardSlot | None, slotIsFacedown: bool, drawnCard: Card, newDiscard: Card) -> None:
        # slot is None if the drawn card was discarded
        return # No implementation for default implementation