import random
from typing import List
from Card import Card
from CardSlot import CardSlot
from GameState import GameState
from GolfHand import GolfHand
from Player import Player
from PlayerType import PlayerType
from TurnResult import TurnResult


class Pair:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column


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
    def __init__(self, playerIndex: int):
        super().__init__(random_name(), PlayerType.AI, playerIndex)
        self.__maxToleratedScore = 10  # AI will try to keep score below this value
        self.__maxToleratedCard = 5  # AI will try to avoid cards with value above this

    def initialReveal(self) -> None:
        self.hand.revealCard(1, 0)
        self.hand.revealCard(1, 1)

    def playTurn(self, gameState: GameState) -> TurnResult:
        currentScore = self.hand.calculate_current_hand_value()
        facedownCount = self.__getFacedownCount()
        
        # determine if the discard matches any of the AI's revealed cards
        discard_card = gameState.cardDeck.topDiscardCard()

        # analyze card potential
        potentialSlot = self.__analyzeCardPotential(discard_card, facedownCount, currentScore)

        if potentialSlot is not None:
            # take the discard card
            card = gameState.cardDeck.takeDiscardCard()
            newDiscard = potentialSlot.card
            self.hand.placeRevealedCard(potentialSlot.row, potentialSlot.column, card)
            return TurnResult(gameState, True, None, False, potentialSlot.row, potentialSlot.column, newDiscard)
        
        # draw from the deck
        drawnCard = gameState.cardDeck.draw_card()

        potentialSlot = self.__analyzeCardPotential(drawnCard, facedownCount, currentScore)

        if potentialSlot is not None:
            # take the drawn card
            newDiscard = potentialSlot.card
            self.hand.placeRevealedCard(potentialSlot.row, potentialSlot.column, drawnCard)
            return TurnResult(gameState, False, drawnCard, True, potentialSlot.row, potentialSlot.column, newDiscard)

        # discard the drawn card
        gameState.cardDeck.discard(drawnCard)

        return TurnResult(gameState, False, drawnCard, False, -1, -1, drawnCard)

    def watchTurn(self, originalState: GameState, playerIndex: int, turnResult: TurnResult) -> None:
        pass # No implementation for default implementation


    def __analyzeCardPotential(self, card: Card, unrevealedCount: int, currentScore: int) -> CardSlot | None:
        worstCardValue = -100
        worstSlot = None
        fakeSlot = CardSlot(0, 0)
        fakeSlot.placeRevealedCard(card)
        faceDownSlots: List[CardSlot] = []

        for row in range(2):
            for col in range(3):
                slot = self.hand.getSlot(row, col)
                mirror = self.hand.getSlot(1 - row, col)

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
        if worstSlot is not None and fakeSlot.get_card_value() < self.__maxToleratedCard and fakeSlot.get_card_value() < worstCardValue:
            return worstSlot
        
        # is the card good enough to take
        if faceDownSlots.__len__() > 1 and fakeSlot.get_card_value() < self.__maxToleratedCard:
            return faceDownSlots[0]
        
        return None
    
    def __calculatePotentialHandScore(self, newCard: Card, replaceSlot: CardSlot) -> int:
        potentialHand = self.hand.clone()
        potentialHand.placeRevealedCard(replaceSlot.row, replaceSlot.column, newCard)
        return potentialHand.calculate_current_hand_value()
    
    def __getFacedownCount(self) -> int:
        count = 0
        for row in range(2):
            for col in range(3):
                slot = self.hand.getSlot(row, col)
                if  slot.isFaceDown:
                    count += 1
        return count