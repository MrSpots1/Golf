

from Logger import Logger
from AIPlayer import AIPlayer
from AggressiveAIPlayer import AggressiveAIPlayer
from GolfManager import GolfManager


class TournamentLogger(Logger):
    def __init__(self):
        super().__init__()
        self.wins = None
        self.ties = 0

    def Result(self, players: list) -> None:
        if self.wins is None:
            self.wins = [0] * len(players)
        winningScore = 1000
        winningIndex = -1

        for i, player in enumerate(players):
            score = player.hand.calculate_current_hand_value()
            print(f"{player.name} scored {score} points.")
            if score < winningScore:
                winningScore = score
                winningIndex = i
            elif score == winningScore:
                winningIndex = -1  # tie
        if winningIndex == -1:
            self.ties += 1
        else:
            self.wins[winningIndex] += 1

    def FinalWins(self, players: list) -> None:
        print("\n=== Tournament Results ===")
        for i, player in enumerate(players):
            print(f"{player.name} won {self.wins[i]} rounds.")
        print(f"Ties: {self.ties}")


class Tournament:
    def __init__(self):
        self.players = [AIPlayer(), AggressiveAIPlayer(maxToleratedCard=10)]
        self.rounds = 200

    def run(self):
        logger = TournamentLogger()
        for round in range(self.rounds):
            print(f"\n=== Tournament Round {round + 1} ===")
            manager = GolfManager(self.players, logger)
            manager.run()
        logger.FinalWins(self.players)

