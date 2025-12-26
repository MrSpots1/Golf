import random
from typing import List
from Card import Card
from CardSlot import CardPosition, CardSlot
from GameState import GameState
from GolfHand import GolfHand
from Player import Player
from PlayerType import PlayerType
from TurnResult import TurnAction, TurnResult

def random_name():
    base_names = [
        "Alice", "Bob", "Charlie", "Daisy", "Eve",
        "Frank", "Grace", "Henry", "Ivy", "Jack"
    ]

    adjectives = [
        "", "", "",  # increase chance of no adjective
        "Fancy", "Happy", "Swift", "Clever", "Brave",
        "Sunny", "Lucky", "Chill"
    ]

    return random.choice(adjectives) + random.choice(base_names)

class AIPlayer(Player):
    def __init__(self, maxToleratedScore: int = 10, maxToleratedCard: int = 5):
        super().__init__(random_name(), PlayerType.AI)
        self.__maxToleratedScore = maxToleratedScore  # AI will try to keep score below this value
        self.__maxToleratedCard = maxToleratedCard  # AI will try to avoid cards with value above this

    def initialReveal(self) -> None:
        self.hand.revealCard(CardPosition(1, 0))
        self.hand.revealCard(CardPosition(1, 1))

    def considerDiscardCard(self, gameState: GameState, card: Card) -> CardSlot | None:
        currentScore = self.hand.calculate_current_hand_value()
        facedownCount = self.__getFacedownCount()        
        return self.__analyzeCardPotential(card, facedownCount, currentScore)

    def considerDrawCard(self, gameState: GameState, card: Card) -> CardSlot | None:
        currentScore = self.hand.calculate_current_hand_value()
        facedownCount = self.__getFacedownCount()        
        return self.__analyzeCardPotential(card, facedownCount, currentScore)
    
    def watchDiscard(self, gameState: GameState, slot: CardSlot | None, discardCard: Card | None, newDiscard: Card | None) -> None:
        # slot, discardCard, and newDiscard are all None if the discard card was not taken
        # all have vaues if it is taken
        return # No implementation for default implementation
    
    def watchDraw(self, gameState: GameState, slot: CardSlot | None, drawnCard: Card, newDiscard: Card) -> None:
        # slot is None if the drawn card was discarded
        return # No implementation for default implementation

    def __analyzeCardPotential(self, card: Card, unrevealedCount: int, currentScore: int) -> CardSlot | None:
        worstCardValue = -100
        worstSlot = None
        fakeSlot = CardSlot(CardPosition(0, 0))
        fakeSlot.placeRevealedCard(card)
        faceDownSlots: List[CardSlot] = []

        for row in range(2):
            for col in range(3):
                slot = self.hand.getSlot(row=row, column=col)
                mirror = self.hand.getSlot(row=1 - row, column=col)

                if slot.isFaceDown:
                    faceDownSlots.append(slot)

                # determine if it's the last unrevealed card
                if unrevealedCount == 1 and slot.isFaceDown:
                     potentialScore = self.__calculatePotentialHandScore(card, slot)
                     if potentialScore <= self.__maxToleratedScore:
                         return slot
                
                # determine if there is a match with the mirror
                if (slot.isFaceDown or slot.card.type != card.type) and not mirror.isFaceDown and mirror.card.type == card.type:
                    return slot
                
                # determine if we should consider this an isolated worst card
                if not slot.isFaceDown and ((not mirror.isFaceDown and slot.card.type != mirror.card.type) or mirror.isFaceDown):
                    cardValue = slot.get_card_value()
                    if cardValue > worstCardValue:
                        worstCardValue = cardValue
                        worstSlot = slot    
                        
        # is there a worst slot to replace that is below max tolerated card value
        if worstSlot is not None and fakeSlot.get_card_value() <= self.__maxToleratedCard and fakeSlot.get_card_value() < worstCardValue:
            return worstSlot
        
        # is the card good enough to take
        if faceDownSlots.__len__() > 1 and fakeSlot.get_card_value() < self.__maxToleratedCard:
            return faceDownSlots[0]
        
        return None
    
    def __calculatePotentialHandScore(self, newCard: Card, replaceSlot: CardSlot) -> int:
        potentialHand = self.hand.clone()
        potentialHand.placeRevealedCard(CardPosition(replaceSlot.row, replaceSlot.column), newCard)
        return potentialHand.calculate_current_hand_value()
    
    def __getFacedownCount(self) -> int:
        count = 0
        for row in range(2):
            for col in range(3):
                slot = self.hand.getSlot(row=row, column=col)
                if  slot.isFaceDown:
                    count += 1
        return count