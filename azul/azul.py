import random
from player import Player
from factory import Factory, Center
class Azul:
    def __init__(self, num_players, player_list=None):
        self.num_players = num_players
        self.players = player_list or [Player(player_id) for player_id in range(num_players)]
        self.first_player_marker_owner = random.choice(self.players)
        print("Initial first player marker owner:", self.first_player_marker_owner)
        self.tile_bag = []
        # self.factories = [Factory(ind) for ind in range(num_players * 2 + 1)]
        self.factories = [Factory(ind) for ind in range(5)]
        self.center = Center()
        self.factories_dict = {"Factory %d" % i: self.factories[i] for i in range(5)}
        self.factories_dict["Center"] = self.center
        self.current_round = 0
        self.game_over = False
        self.tile_bag = self.generate_tile_bag()
        self.refill_factories()
        self.current_player = self.first_player_marker_owner

    def to_dict(self):
        return {
            'factories': [factory.to_dict() for factory in self.factories],
            'center': self.center.to_dict(),
            'players': [player.to_dict() for player in self.players],
            'currentPlayer': str(self.current_player.player_id)
        }

    def generate_tile_bag(self):
        tile_colors = ['blue', 'red', 'yellow', 'black', 'white']
        tile_bag = [color for color in tile_colors for _ in range(20)]
        random.shuffle(tile_bag)
        return tile_bag

    def refill_factories(self):
        for factory in self.factories:
            for _ in range(4):
                if not self.tile_bag:
                    self.tile_bag = self.generate_tile_bag()
                factory.add_tile(self.tile_bag.pop())

    def get_available_actions(self, player):
        available_actions = []
        for source_type, source in [("factory", f) for f in self.factories] + [("center", self.center)]:
            tiles = source.tiles

            # print("source_type")
            for color in set(tiles):
                if color == "1":
                    # First player marker is not a valid color
                    continue

                # Find the pattern line indices that the player can place the tile on
                print("player.pattern_lines",player.pattern_lines)
                valid_pattern_line_indices = [
                    idx for idx, _ in enumerate(player.pattern_lines)
                    if player.can_place_tile_on_pattern_line(color, idx)
                ]
                # Generate actions for each combination of source, color, and valid pattern line index
                for pattern_line_idx in valid_pattern_line_indices:
                    available_actions.append((source_type, source, color, pattern_line_idx))

        return available_actions

    def get_available_sources(self):
        available_source = []
        for factory in self.factories:
            if len(factory.tiles) > 0:
                available_source.append(factory)
        if len(self.center.tiles) > 0:
            available_source.append(self.center)

        return available_source

    def get_available_colors(self, source):
        available_colors = {}
        if isinstance(source, Factory):
            for ind, color in enumerate(set(source.tiles)):
                available_colors[ind] = color
        else:
            for ind, color in enumerate(set(source.tiles)):
                available_colors[ind] = color
        return available_colors

    def get_available_pattern_lines(self, player, color):
        available_pattern_lines = []
        for pattern_line_idx, pattern_line in enumerate(player.pattern_lines):
            if player.can_place_tile_on_pattern_line(color, pattern_line_idx):
                available_pattern_lines.append(pattern_line_idx)
        available_pattern_lines.append(-1) # representing floor line
        return available_pattern_lines


    def move_remaining_tiles_to_center_area(self, source):
        remaining_tiles = source.remove_all_tiles()
        print("remaining tiles")
        print(remaining_tiles)
        # print(type(self.central_area))
        self.center.add_tile(remaining_tiles)

    def perform_action(self, player, source, color, pattern_line_idx):

        tiles_taken = source.take_tiles(color)
        if pattern_line_idx != -1:
            player.add_tiles_to_pattern_line(color, tiles_taken, pattern_line_idx)
        else:
            player.add_tiles_to_floor_line(tiles_taken)

        if not source.is_center():
            self.move_remaining_tiles_to_center_area(source)

        if source.is_center() and self.first_player_marker_owner is None:
            self.first_player_marker_owner = player
            print("player", player.player_id, "is the first player next round")
            player.floor_line.append("F")
        print("now your pattern lines are", player.pattern_lines)
        print("now your floor line is", player.floor_line)

    def get_winner(self):
        # Calculate the final scores for all players
        for player in self.players:
            player.calculate_final_score()

        # Sort the players by their scores, descending
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)

        # If there is no tie, return the player with the highest score
        if sorted_players[0].score != sorted_players[1].score:
            return sorted_players[0]

        # Tiebreaker 1: Most completed horizontal rows
        players_with_most_rows = [player for player in sorted_players if
                                  player.completed_rows() == max(p.completed_rows() for p in sorted_players)]
        if len(players_with_most_rows) == 1:
            return players_with_most_rows[0]

        # Tiebreaker 2: Fewest total tiles in the floor line
        players_with_fewest_floor_tiles = [player for player in players_with_most_rows if len(player.floor_line) == min(
            len(p.floor_line) for p in players_with_most_rows)]
        if len(players_with_fewest_floor_tiles) == 1:
            return players_with_fewest_floor_tiles[0]

        # If there is still a tie, the victory is shared
        return players_with_fewest_floor_tiles

    def play_round(self):
        while not self.is_round_over():
            for player in self.players:
                action = player.play_turn(self)
                self.perform_action(player, action)
        self.end_round()

    def is_round_over(self):
        return all(factory.is_empty() for factory in self.factories) and self.center.is_empty()

    # def end_round(self):
    #     for player in self.players:
    #         player.transfer_tiles()
    #         player.clear_pattern_lines()
    #         player.clear_floor_line()
    #
    #     if any(player.check_horizontal_row_completed() for player in self.players):
    #         self.game_over = True
    #
    #     self.refill_factories()
    #     self.current_round += 1

    # Implement other methods as needed for the Azul game environment

    def end_round(self):
        for player in self.players:
            player.move_tiles_from_pattern_lines_to_wall()

            player.deduct_floor_line_points()

        # Check if the first player marker has been taken
        for player in self.players:
            if player.floor_line[0] == 'F':
                # player.floor_line[0] = False
                self.first_player_marker_owner = player
                break
            player.floor_line = []

        # Refill factories
        self.refill_factories()

        # Check if the game has ended
        game_has_ended = any(player.check_wall_for_completed_rows() for player in self.players)
        if game_has_ended:
            for player in self.players:
                player.add_bonus_points()
            self.winner = self.get_winner()
        # else:
        #     self.start_new_round()


    def start_new_round(self):
        # Determine the starting player
        print("First player marker owner before starting new round:", self.first_player_marker_owner)
        starting_player = self.players.index(self.first_player_marker_owner)

        # Reset the "1st Player" marker owner for the next round
        self.first_player_marker_owner = None

        # Refill the factories and central area
        self.refill_factories_and_central_area()

        return starting_player

    def refill_factories_and_central_area(self):
        # Refill the tile bag if it's empty
        if len(self.tile_bag) == 0:
            self.tile_bag = self.create_tile_bag()

        # Refill the factories
        for factory in self.factories:
            while len(factory.tiles) < 4:
                tile = self.tile_bag.pop()
                factory.tiles.append(tile)

        # Refill the central area
        self.center = Center()

    def is_game_over(self):
        for player in self.players:
            if any(all(cell is not None for cell in row) for row in player.wall):
                return True
        return False

