# game.py

from splendor import Splendor, Player

def main():
    # Initialize the game
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game = Splendor([player1, player2])

    # Main game loop
    while True:
        for player in game.players:
            game.player_turn(player)

            # Check for the end of the game
            if player.points >= 15:
                print(f"{player.name} wins!")
                return

if __name__ == "__main__":
    main()
