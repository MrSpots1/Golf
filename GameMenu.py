from AIPlayer import AIPlayer
from GolfManager import GolfManager
from HumanPlayer import HumanPlayer
from Tournament import Tournament


class GameMenu: 
    def display(self):
        print("\n=== Golf: Main Menu ===")
        print("1) Start new game vs AI")
        print("2) Start new game vs Player")
        print("3) Start new Tournament")
        print("4) Show Rules")
        print("q) Quit")

    def run(self):
        running = True
        while running:
            self.display()
            choice = input("Select an option (1-4 or q): ").strip().lower()
            match choice:
                case "1":
                    self.on_ai_start()
                case "2":
                    self.on_player_start()
                case "3":
                    self.on_tournament_start()
                case "4":
                    self.on_show_rules()
                case "q":
                    print("Goodbye!")
                    running = False
                case _:
                    print("Invalid selection. Please try again.\n")

    def on_ai_start(self):
        taylan = HumanPlayer("Taylan")
        ai = AIPlayer()
        manager = GolfManager([taylan, ai])
        manager.run()

    def on_tournament_start(self):
        tourney = Tournament()
        tourney.run()

    def on_player_start(self):
        players = []
        while True:
            player_amount = input("Please input the player count: ")
            try:
                player_amount = int(player_amount)
            except ValueError:
                print("Invalid input. Please try again.")
                continue
            if player_amount < 2:
                print("Invalid input. Please try again.")
                continue
            break
        player_names = []
        for i in range(player_amount):
            while True:
                name = input(f"Please enter Player {i+1}'s name: ")
                if name.lower() not in player_names:
                    player_names.append(name.lower())
                    break
                print("Name already in use. Please try again.")
            players.append(HumanPlayer(name))

        manager = GolfManager(players)
        manager.run()

    def on_show_rules(self):
        print("\n--- Golf Rules (Simplified) ---")
        print("Goal: Finish with the lowest total score.")
        print("Each player has a 2 row by 3 column grid of cards; lower values are better.")
        print("On your turn, draw from the deck or discard to improve your grid.")
        print("Scoring:")
        print("  - When both cards in a column match, they count for 0 points (except for 2s).")
        print("  - Twos count for -2 points off your score.")
        print("  - Aces count for 1 point.")
        print(" - Kings count as zero points.")
        print(" - Jacks and Queens count as 10 points.")
        print("  - Other number cards count as their face value.")
        print("Round ends when a player has all cards face-up; score is tallied.")
