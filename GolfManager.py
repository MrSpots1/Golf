from CardSlot import CardPosition
from CardSuit import CardSuit
from CardType import CardType
from Card import Card
from GameState import GameState
from Logger import ConsoleLogger, Logger
from Player import Player
from PlayerType import PlayerType
from CardDeck import CardDeck

class GolfManager:
    def __init__(self, players: list, logger: Logger = ConsoleLogger()):
        self.deck = CardDeck(2)
        self.deck.shuffle()
        self.__logger = logger

        self.players = players
        self.currentPlayerIndex = 0

    def deal(self):
        # for each player, deal 6 cards face down
        for player in self.players:
            for r in range(player.hand.rows):
                for c in range(player.hand.columns):
                    card = self.deck.draw_card()
                    player.hand.placeFacedownCard(CardPosition(r, c), card)
        
        # provide a first discard card
        firstDiscard = self.deck.draw_card()
        self.deck.discard(firstDiscard)

    def isGameOver(self):
        for player in self.players:
            if player.hand.is_done():
                return True
        return False

    def displayPlayer(self, player:Player, isTurn: bool, displayScore: bool = False):
        turn_marker = "-> " if isTurn else ""
        self.__logger.Info(f"\n{turn_marker}{player.name}:")
        self.__logger.Info(player.hand.str())
        if displayScore:
            self.__logger.Info(f"Score: {player.hand.calculate_current_hand_value()}")
        
    def displayGameState(self, gameState: GameState, displayScores: bool = False):
        self.__logger.Info("\nCurrent Game State:")
        for p in range(len(gameState.players)):
            self.displayPlayer(gameState.players[p], (p == gameState.playerIndex), displayScores)            
        self.__logger.Info(f"\nTop discard card: {gameState.cardDeck.topDiscardCard().str()}\n")

    def run(self):
        for player in self.players:
            player.initializeHand()

        self.deal()
        out_player_index = -1
        # allow all players to pick two cards to reveal initially
        for player in self.players:
            player.initialReveal()

        # allow all players to observe the initial game state
        for player in self.players:
            player.observeGameState(GameState(self.deck, self.players, self.currentPlayerIndex))

        while not self.isGameOver() or self.isGameOver() and self.currentPlayerIndex != out_player_index:
            currentPlayer = self.players[self.currentPlayerIndex]
            gameState = GameState(self.deck, self.players, self.currentPlayerIndex)
            self.displayGameState(gameState)
            self.__logger.Info(f"It is {currentPlayer.name}'s turn.")

            takenCard = None
            newDiscard = None
            
            # let current player consider the top discard card
            played_slot = currentPlayer.considerDiscardCard(gameState, gameState.cardDeck.topDiscardCard())
            slotIsFacedown = False
            if played_slot is not None:
                takenCard = gameState.cardDeck.takeDiscardCard()
                newDiscard = played_slot.card
                slotIsFacedown = played_slot.isFaceDown
                currentPlayer.hand.placeRevealedCard(played_slot.position, takenCard)
                self.__logger.Info(f"{currentPlayer.name} took the {takenCard.str()} and played it in position ({played_slot.position.row + 1}, {played_slot.position.column + 1}), discarding {newDiscard.str()}.")
                self.deck.discard(newDiscard)
            else:
                self.__logger.Info(f"{currentPlayer.name} did not take the {gameState.cardDeck.topDiscardCard().str()}. Drawing...")
                
            # notify all players about the discard action
            for i, player in enumerate(self.players):
                if i != self.currentPlayerIndex:
                    player.watchDiscard(gameState, played_slot, slotIsFacedown, takenCard, newDiscard)

            if played_slot is None:
                # let current player consider drawing a new card
                drawnCard = gameState.cardDeck.draw_card()
                self.__logger.Info(f"{currentPlayer.name} drew a {drawnCard.str()}.")
                played_slot = currentPlayer.considerDrawCard(gameState, drawnCard)

                if played_slot is not None:
                    newDiscard = played_slot.card
                    slotIsFacedown = played_slot.isFaceDown
                    currentPlayer.hand.placeRevealedCard(played_slot.position, drawnCard)
                    self.__logger.Info(f"{currentPlayer.name} drew the {drawnCard.str()} and played it in position ({played_slot.position.row + 1}, {played_slot.position.column + 1}), discarding {newDiscard.str()}.")
                    self.deck.discard(newDiscard)
                else:
                     self.deck.discard(drawnCard)
                     self.__logger.Info(f"{currentPlayer.name} discarded the {drawnCard.str()}.")

                # notify all players about the draw action
                for i, player in enumerate(self.players):
                    if i != self.currentPlayerIndex:
                        player.watchDraw(gameState, played_slot, slotIsFacedown, drawnCard, newDiscard)
               
            if currentPlayer.hand.is_done() and out_player_index == -1:
                out_player_index = self.currentPlayerIndex

            # move to next player
            self.currentPlayerIndex = (self.currentPlayerIndex + 1) % len(self.players)
        
        self.__logger.Info("The game is over!")

        winner = None
        winningScore = 100000
        for player in self.players:
            player.hand.revealRemainingCards()

        self.__logger.Info("The final game state is as follows: ")
        gameState = GameState(self.deck, self.players, self.currentPlayerIndex)
        self.displayGameState(gameState, displayScores=True)

        self.__logger.Result(self.players)
        
