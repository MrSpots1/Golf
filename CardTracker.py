from CardType import CardType
from Card import Card

class CardTracker:
    def __init__(self, deckCount: int):
        self.deckCount = deckCount
        # Initialize an array of ints, all zeros, one for each value of a card
        self.__counts = [0] * (len(CardType))
        self.__maxCountPerType = deckCount * 4  # 4 suits per type
        self.__totalCards = deckCount * 52  # 52 cards per deck

    def observeCard(self, card: Card) -> None:
        self.__counts[card.type.value - 1] += 1

    def getObservedCount(self, cardType: CardType) -> int:
        observedCount = self.__counts[cardType.value - 1]
        return observedCount

    def getRemainingCount(self, cardType: CardType) -> int:
        observedCount = self.__counts[cardType.value - 1]
        return self.__maxCountPerType - observedCount
    
    def getTotalRemainingCards(self) -> int:
        observedTotal = sum(self.__counts)
        return self.__totalCards - observedTotal
    
    def getProbabilityOfDrawing(self, cardType: CardType) -> float:
        remainingCount = self.getRemainingCount(cardType)
        totalRemaining = self.getTotalRemainingCards()
        if totalRemaining == 0:
            return 0.0
        return remainingCount / totalRemaining
