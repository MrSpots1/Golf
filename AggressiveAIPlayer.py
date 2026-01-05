import random
from typing import List
from AIPlayer import AIPlayer
from Card import Card
from CardSlot import CardPosition, CardSlot
from CardTracker import CardTracker
from CardType import CardType
from GameState import GameState
from GolfHand import GolfHand
from Player import Player
from PlayerType import PlayerType
from TurnResult import TurnAction, TurnResult


class AggressiveAIPlayer(AIPlayer):
    def __init__(self, maxToleratedScore: int = 10, maxToleratedCard: int = 7):
        super().__init__(maxToleratedScore, maxToleratedCard)

    def considerDiscardCard(self, gameState: GameState, card: Card) -> CardSlot | None:
        currentScore = self.hand.calculate_current_hand_value()
        facedownCount = self._getFacedownCount()        
        return self._analyzeCardPotential(gameState, card, False, facedownCount, currentScore)

    def considerDrawCard(self, gameState: GameState, card: Card) -> CardSlot | None:
        currentScore = self.hand.calculate_current_hand_value()
        facedownCount = self._getFacedownCount()
        nextPlayerWantsCard = self._isSafeDiscard(card, gameState)        
        return self._analyzeCardPotential(gameState, card, nextPlayerWantsCard, facedownCount, currentScore)
    
    def _analyzeCardPotential(self, gameState: GameState, card: Card, nextPlayerWantsCard: bool, unrevealedCount: int, currentScore: int) -> CardSlot | None:
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
                     if self._shouldGoOut(gameState, card, slot):
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

        # if there is more than one facedown slot, just play the card
        if faceDownSlots.__len__() > 1 and fakeSlot.get_card_value() < self._maxToleratedCard:
            return faceDownSlots[0]
        
        # is there a worst slot to replace that is below max tolerated card value, or if the next player wants the card
        # TODO: consider probability of there still being a match in the future
        if worstSlot is not None and ((fakeSlot.get_card_value() <= self._maxToleratedCard and fakeSlot.get_card_value() < worstCardValue) or nextPlayerWantsCard):
            return worstSlot

        return None
    
    def _shouldGoOut(self, gameState: GameState, card: Card, slot: CardSlot) -> bool:
        potentialScore = self._calculatePotentialHandScore(card, slot)
        if potentialScore <= self._maxToleratedScore:
            return slot
    
    def _nextPlayerHasMatch(self, card: Card, gameState: GameState) -> bool:
        nextPlayerIndex = (gameState.playerIndex + 1) % len(gameState.players)
        nextPlayer = gameState.players[nextPlayerIndex]

        for row in range(2):
            for col in range(3):
                slot = nextPlayer.hand.getSlot(row=row, column=col)
                mirror = nextPlayer.hand.getSlot(row=1 - row, column=col)
                if not slot.isFaceDown and slot.card.type == card.type and \
                    (mirror.isFaceDown or mirror.card.type != card.type):
                    return True
        return False
    
    def _isGoodCard(self, card: Card) -> bool:
        return card.type in [CardType.Two, CardType.King, CardType.Ace]

    def _isSafeDiscard(self, card: Card, gameState: GameState) -> bool:
        return self._nextPlayerHasMatch(card, gameState) and not self._isGoodCard(card)
    
    def _calculatePotentialHandScore(self, newCard: Card, replaceSlot: CardSlot) -> int:
        potentialHand = self.hand.clone()
        potentialHand.placeRevealedCard(CardPosition(replaceSlot.position.row, replaceSlot.position.column), newCard)
        return potentialHand.calculate_current_hand_value()
    
    def _getFacedownCount(self) -> int:
        count = 0
        for row in range(2):
            for col in range(3):
                slot = self.hand.getSlot(row=row, column=col)
                if  slot.isFaceDown:
                    count += 1
        return count
    
    def _calculate_current_hand_value(self) -> int:
        score = 0
        for c in range(self.hand.columns):
            for r in range(self.hand.rows):
                slot = self.hand.getSlot(row=r, column=c)
                mirror = self.hand.getSlot(row=1 - r, column=c)
                if slot.isFaceDown:
                    score += self._estimate_facedown_card_value()
                elif mirror.isFaceDown:
                    score += slot.get_card_value()
                else:
                    if slot.card.type == mirror.card.type and slot.card.type != CardType.Two:
                        score += 0
                    else:
                        score += slot.get_card_value()
        return score
    
    def _estimate_facedown_card_value(self) -> int:
        return 10
