
class Logger:
    def __init__(self):
        pass

    def Info(self, message: str) -> None:
        pass

    def Warning(self, message: str) -> None:
        pass

    def Error(self, message: str) -> None:
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