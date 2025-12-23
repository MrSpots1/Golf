from GameMenu import GameMenu

def main():
	menu = GameMenu()
	menu.run()
try:
	main()
except KeyboardInterrupt:
	print("\nGoodbye!")
