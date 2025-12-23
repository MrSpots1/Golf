from CardSuit import CardSuit
from CardType import CardType
from Card import Card
from GameState import GameState
from PlayerType import PlayerType
from CardDeck import CardDeck

class GolfManager:
    def __init__(self, players: list):
        self.deck = CardDeck(2)
        self.deck.shuffle()

        self.players = players
        self.currentPlayerIndex = 0

    def deal(self):
        # for each player, deal 6 cards face down
        for player in self.players:
            for r in range(player.hand.rows):
                for c in range(player.hand.columns):
                    card = self.deck.draw_card()
                    player.hand.placeHiddenCard(r, c, card)
        
        # provide a first discard card
        firstDiscard = self.deck.draw_card()
        self.deck.discard(firstDiscard)

    def isGameOver(self):
        for player in self.players:
            if player.hand.is_done():
                return True
        return False

    def displayGameState(self, gameState: GameState):
        print("Current Game State:")
        for p in range(len(gameState.players)):
            isTurn = (p == gameState.playerIndex)
            gameState.players[p].display(isTurn)
        print(f"Top discard card: {gameState.cardDeck.topDiscardCard().display()}")
    def displayFinalGameState(self, gameState: GameState):
        for p in range(len(gameState.players)):
            gameState.players[p].displayFinal(False)
            print("Hand Value:", gameState.players[p].hand.calculate_current_hand_value(), "\n")

    def run(self):
        self.deal()
        out_player_index = -1
        # allow them to pick two cards to reveal initially
        for player in self.players:
            player.initialReveal()

        while not self.isGameOver() or self.isGameOver() and self.currentPlayerIndex != out_player_index:
            currentPlayer = self.players[self.currentPlayerIndex]
            gameState = GameState(self.deck, self.players, self.currentPlayerIndex)
            self.displayGameState(gameState)
            print(f"It is {currentPlayer.name}'s turn.")
            print("\n")
            turnResult = currentPlayer.playTurn(gameState)

            # display the move if it is AI
            if currentPlayer.playerType != PlayerType.Human:
                print(f"{currentPlayer.name} played their turn:")
                print(turnResult.describe())
                print("\n")

            # allow the other players to watch/observe that move
            for i, player in enumerate(self.players):
                if i != self.currentPlayerIndex:
                    player.watchTurn(gameState, self.currentPlayerIndex, turnResult)
            if currentPlayer.hand.is_done() and out_player_index == -1:
                out_player_index = self.currentPlayerIndex
            # move to next player
            self.currentPlayerIndex = (self.currentPlayerIndex + 1) % len(self.players)

        
        print("The game is over!")

        winner = None
        winningScore = 100000
        for player in self.players:
            player.hand.revealRemainingCards()

            score = player.hand.calculate_current_hand_value()
            print(f"{player.name} scored {score} points.")
            if score < winningScore:
                winningScore = score
                winner = player
        print("The final game state is as follows: ")
        gameState = GameState(self.deck, self.players, self.currentPlayerIndex)
        self.displayFinalGameState(gameState)
        print(f"The winner is {winner.name} with a score of {winningScore} points!")
        


