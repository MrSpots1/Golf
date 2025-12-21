from CardSlot import CardSlot
from CardSuit import CardSuit
from CardType import CardType
from CardClass import Card

class GolfHand:
    def __init__(self, rows: int = 2, columns: int = 3):
        self.slots = []
        self.rows = rows
        self.columns = columns

        for r in range(rows):
            self.slots.append([])
            for c in range(columns):
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

    def display(self):
        display_string = ""
        for r in range(self.rows):
            for c in range(self.columns):
                display_string += self.slots[r][c].display() + " "
            display_string += "\n"
        print(display_string)

    