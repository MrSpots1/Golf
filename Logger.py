
class Logger:
    def __init__(self):
        pass

    def Info(self, message: str) -> None:
        pass

    def Warning(self, message: str) -> None:
        pass

    def Error(self, message: str) -> None:
        pass

    def Result(self, players: list) -> None:
        pass

class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def Info(self, message: str) -> None:
        print(f"{message}")

    def Warning(self, message: str) -> None:
        print(f"[WARNING] {message}")

    def Error(self, message: str) -> None:
        print(f"[ERROR] {message}")

    def Result(self, players: list) -> None:
        winningScore = 1000
        winner = None
        for player in players:
            score = player.hand.calculate_current_hand_value()
            self.Info(f"{player.name} scored {score} points.")
            if score < winningScore:
                winningScore = score
                winner = player
        self.Info(f"The winner is {winner.name} with a score of {winningScore} points!")