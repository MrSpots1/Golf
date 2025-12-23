from CardSlot import CardSlot
from CardSuit import CardSuit
from CardType import CardType
from Card import Card

class GolfHand:
    def __init__(self):
        self.slots = []
        self.rows = 2
        self.columns = 3

        for r in range(self.rows):
            self.slots.append([])
            for c in range(self.columns):
                self.slots[r].append(CardSlot())

    def getSlot(self, row: int, column: int) -> CardSlot:
        if row < 0 or row >= self.rows:
            raise IndexError("Row index out of range")
        if column < 0 or column >= self.columns:
            raise IndexError("Column index out of range")
        return self.slots[row][column]
    
    def placeHiddenCard(self, row: int, column: int, card: Card):
        self.getSlot(row, column).placeHiddenCard(card)

    def revealCard(self, row: int, column: int):
        self.getSlot(row, column).revealCard()
    
    def placeRevealedCard(self, row: int, column: int, card: Card):
        self.getSlot(row, column).placeRevealedCard(card)

    def display(self, ending_new_line = False):
        display_string = ""
        for r in range(self.rows):
            for c in range(self.columns):
                display_string += self.slots[r][c].display() + " "
            display_string += "\n"
        if ending_new_line:
            display_string = display_string[:-1]
        print(display_string)

    def revealRemainingCards(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.slots[r][c].isFaceDown:
                    self.slots[r][c].revealCard()

    def calculate_current_hand_value(self):
        score = 0
        for c in range(self.columns):
            if not self.slots[0][c].isFaceDown and not self.slots[1][c].isFaceDown:
                if self.slots[0][c].card.type == self.slots[1][c].card.type and self.slots[0][c].card.type != CardType.Two:
                    continue
                else:
                    score += self.slots[0][c].get_card_value()
                    score += self.slots[1][c].get_card_value()
            elif self.slots[0][c].isFaceDown and not self.slots[1][c].isFaceDown:
                score += self.slots[1][c].get_card_value()
            elif not self.slots[0][c].isFaceDown and self.slots[1][c].isFaceDown:
                score += self.slots[0][c].get_card_value()
            else:
                continue
        return score

    def is_done(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.slots[r][c].isFaceDown:
                    return False
        return True
