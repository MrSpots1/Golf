from CardClass import Card
import CardDeck

class GameState:
    def __init__(self, cardDeck: CardDeck, players: list, playerIndex: int):
        self.cardDeck = cardDeck
        self.players = players
        self.playerIndex = playerIndex
