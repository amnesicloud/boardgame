import sys
from azul import Azul
from player import HumanPlayer, RLPlayer

def play_azul(player1, player2):
    game = Azul(num_players=2, player_list=[player1, player2])
    game.start_new_round()
    while not game.is_game_over():
        print("*" * 50)
        print("new round")
        while not game.is_round_over():
            for ind in range(game.num_players):
                print(game.player_dict)
                print(game.player_dict.keys())
                player = game.player_dict[(game.first_player_marker_owner_id + ind) % game.num_players]
                print("=" * 50)
                print("player%d's turn" % player.player_id)
                print("player%d's score is" % player.player_id, player.score)
                print("player%d's pattern line is" % player.player_id, player.pattern_lines)
                print("player%d's floor line is" % player.player_id, player.floor_line)
                print("player%d's wall is" % player.player_id, player.wall)
                available_sources = game.get_available_sources()
                source = player.choose_source(available_sources)
                available_colors = game.get_available_colors(source)
                color = player.choose_color(available_colors)
                available_pattern_lines = game.get_available_pattern_lines(player, color)
                pattern_line_idx = player.choose_pattern_line(available_pattern_lines)
                game.perform_action(player, source, color, pattern_line_idx)
                if game.is_round_over():
                    break

        game.end_round()
        print("end round")
        for player in game.players:
            print(player.player_id, ":", player.score)


    winner = game.get_winner()
    print(f"Player {winner + 1} wins the game!")


def main():
    mode = int(input("Select mode:\n1. Human vs. Human\n2. Human vs. RL Agent\n3. RL Agent vs. RL Agent\n"))

    if mode == 1:
        player1 = HumanPlayer(player_id=0)
        player2 = HumanPlayer(player_id=1)
    elif mode == 2:
        player1 = HumanPlayer(player_id=0)
        player2 = RLPlayer(player_id=1)
        # Load RL agent's model here
    elif mode == 3:
        player1 = RLPlayer(player_id=0)
        player2 = RLPlayer(player_id=1)
        # Load RL agents' models here
    else:
        print("Invalid mode selection.")
        sys.exit(1)

    play_azul(player1, player2)

if __name__ == "__main__":
    main()
