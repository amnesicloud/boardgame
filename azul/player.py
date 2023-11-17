from factory import Factory
class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.score = 0
        self.wall = [[None for _ in range(5)] for _ in range(5)]  # Initialize the wall as a 5x5 grid
        self.pattern_lines = [[] for _ in range(5)]  # Initialize the pattern lines as 5 rows of different lengths
        self.floor_line = []
        self.COLORS = [['blue', 'yellow', 'red', 'black', 'white'],
                       ['white', 'blue', 'yellow', 'red', 'black'],
                       ['black', 'white', 'blue', 'yellow', 'red'],
                       ['red', 'black', 'white', 'blue', 'yellow'],
                       ['yellow', 'red', 'black', 'white', 'blue']]

    def calculate_points_for_tile_placement(self, row, col):
        points = 0
        same_row = 0
        same_col = 0

        # Check contiguous tiles in the same row to the left of the placed tile
        for c in range(col - 1, -1, -1):
            if self.wall[row][c] is not None:
                same_row += 1
            else:
                break

        # Check contiguous tiles in the same row to the right of the placed tile
        for c in range(col + 1, 5):
            if self.wall[row][c] is not None:
                same_row += 1
            else:
                break

        # Check contiguous tiles in the same column above the placed tile
        for r in range(row - 1, -1, -1):
            if self.wall[r][col] is not None:
                same_col += 1
            else:
                break

        # Check contiguous tiles in the same column below the placed tile
        for r in range(row + 1, 5):
            if self.wall[r][col] is not None:
                same_col += 1
            else:
                break

        # Calculate the points based on contiguous tiles in the row and column
        if same_row == 0 and same_col == 0:
            points = 1
        if same_row > 0:
            points += same_row + 1
        if same_col > 0:
            points += same_col + 1

        return points


    def check_wall_for_completed_rows(self):
        completed_rows = []
        for row_index, row in enumerate(self.wall):
            if all(cell is not None for cell in row):
                completed_rows.append(row_index)
        return completed_rows

    def to_dict(self):
        return {
            'patternLines': self.pattern_lines,
            'wall': self.wall,
            'floor': self.floor_line,
            'score': self.score
        }

    def completed_rows(self):
        completed_row_count = 0
        for row in self.wall:
            if all(cell is not None for cell in row):
                completed_row_count += 1
        return completed_row_count
    # Add other methods as needed for the Player class

    def calculate_final_score(self):
        # Deduct points for tiles in the floor line
        self.deduct_floor_line_points()

        # Add bonus points
        self.add_bonus_points()

    def deduct_floor_line_points(self):
        # Deduct points according to the floor line tiles
        deductions = [1, 1, 2, 2, 2, 3, 3]

        # print("penalty score is", sum(deductions[min(len(self.floor_line) - 1, len(deductions) - 1)] for _ in range(len(self.floor_line))))
        # self.score -= sum(deductions[min(len(self.floor_line) - 1, len(deductions) - 1)] for _ in range(len(self.floor_line)))
        # print("player", self.player_id,"score is:", self.score)

        deduct_point = 0
        for i in range(len(self.floor_line)):
            if i >= len(deductions):
                break
            deduct_point += deductions[i]

        print("penalty score is", deduct_point)
        self.score -= deduct_point
        print("player", self.player_id,"score is:", self.score)

    def add_bonus_points(self):
        # Add bonus points for completed rows, columns, and sets of all 5 colors
        print("add bonus point")
        completed_rows = sum(1 for row in self.wall if all(cell is not None for cell in row))
        completed_columns = sum(1 for col in range(5) if all(self.wall[row][col] is not None for row in range(5)))
        completed_sets = sum(1 for color in set(cell for row in self.wall for cell in row if cell is not None) if sum(cell == color for row in self.wall for cell in row) == 5)

        self.score += 2 * completed_rows + 7 * completed_columns + 10 * completed_sets
        print("player", self.player_id,"score is:", self.score)

    def can_place_tile_on_pattern_line(self, color, pattern_line_idx):
        pattern_line = self.pattern_lines[pattern_line_idx]

        # Check if there is space in the pattern line
        if pattern_line_idx + 1 - len(pattern_line) == 0:
            return False

        # Check if the pattern line is empty or if the color matches the existing tiles in the pattern line
        if len(pattern_line) == 0 or pattern_line[0] is None or pattern_line[0] == color:
            # Check if the corresponding position on the wall is empty
            wall_row_idx = pattern_line_idx
            wall_col_idx = self.COLORS[wall_row_idx].index(color)
            if self.wall[wall_row_idx][wall_col_idx] is None:
                return True

        return False

    def choose_action(self, available_actions):
        while True:
            print("Available actions:")
            print(available_actions)
            for i, action in enumerate(available_actions):
                print(action)
                print(len(action))
                _, source, color, pattern_line_idx = action
                if isinstance(source, Factory):
                    source_name = f"Factory {source.factory_id}"
                else:
                    source_name = "Center area"

                print(f"{i}: {source_name} - {color} - Pattern line {pattern_line_idx + 1}")

            try:
                action_idx = int(input("Choose an action by entering the corresponding number: "))
                if 0 <= action_idx < len(available_actions):
                    return available_actions[action_idx]
                else:
                    print("Invalid input. Please enter a number corresponding to an available action.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def choose_source(self, available_sources):
        pass

    def choose_color(self, available_colors):
        pass

    def choose_pattern_line(self, available_pattern_lines):
        pass

    def print_pattern_lines(self):
        print(f"Player {self.player_id} Pattern Lines:")
        for idx, line in enumerate(self.pattern_lines):
            print(f"{idx + 1}: {line}")

    def print_wall(self):
        print(f"Player {self.player_id} Wall:")
        for row in self.wall:
            print(" ".join(row))

    def print_floor_line(self):
        print(f"Player {self.player_id} Floor Line:")
        print(" ".join(self.floor_line))

    def add_tiles_to_pattern_line(self, color, tiles, pattern_line_idx):
        # Calculate the number of free spaces in the pattern line
        print("pattern_line_idx", type(pattern_line_idx), pattern_line_idx)
        free_spaces = pattern_line_idx + 1 - len(self.pattern_lines[pattern_line_idx])

        # If there are more tiles than free spaces, move the excess tiles to the floor line
        excess_tiles = len(tiles) - free_spaces
        if excess_tiles > 0:
            tiles_to_add = tiles[:-excess_tiles]
            self.floor_line.extend(tiles[-excess_tiles:])
        else:
            tiles_to_add = tiles

        # Add the tiles to the pattern line
        self.pattern_lines[pattern_line_idx].extend(tiles_to_add)

    def add_tiles_to_floor_line(self, tiles):
        self.floor_line.extend(tiles)

    def move_tiles_from_pattern_lines_to_wall(self):
        for pattern_line_idx, pattern_line in enumerate(self.pattern_lines):
            # Check if the pattern line is full
            if len(pattern_line) == pattern_line_idx + 1:
                color = pattern_line[0]

                # Find the corresponding position on the wall
                wall_row_idx = pattern_line_idx
                wall_col_idx = self.COLORS[wall_row_idx].index(color)

                # Move the tile to the wall if the position is empty
                if self.wall[wall_row_idx][wall_col_idx] is None:
                    self.wall[wall_row_idx][wall_col_idx] = color
                    score = self.calculate_points_for_tile_placement(wall_row_idx, wall_col_idx)
                    print("socre added: ", score)
                    self.score += score

                # Clear the pattern line
                self.pattern_lines[pattern_line_idx] = []

class HumanPlayer(Player):
    def get_human_input(self, game):
        print("Player", self.player_id, "turn")
        print("Current game state:")
        print(game)  # Implement a __str__ method for the Game class to display the game state

        available_actions = game.get_available_actions(self)
        print("Available actions:")
        for i, action in enumerate(available_actions):
            print(i, ":", action)

        chosen_action_index = int(input("Choose an action (enter the index): "))
        return available_actions[chosen_action_index]

    def choose_source(self, available_sources):
        while True:
            try:
                for ind, source in enumerate(available_sources):
                    if isinstance(source, Factory):
                        print(ind, "factory ID:", source.factory_id,"tiles", source.tiles)
                    else:
                        print(ind, "factory ID:", source.factory_id,"tiles", source.tiles)
                source_idx = int(input("Choose a source index from available sources: "))
                return available_sources[source_idx]
            except Exception as e:
                print(e)
                print("please re-input")

    def choose_color(self, available_colors):
        while True:
            try:
                for key in available_colors:
                    print(key, available_colors[key])
                color_idx = int(input("Choose a color index from available colors: "))
                return available_colors[color_idx]
            except Exception as e:
                print(e)
                print("please re-input")


    def choose_pattern_line(self, available_pattern_lines):
        while True:
            try:
                for ind, available_pattern_line in enumerate(available_pattern_lines):
                    print(ind, ":", available_pattern_line)
                pattern_line_idx = int(input("Choose a pattern line index from available pattern lines: "))
                return available_pattern_lines[pattern_line_idx]
            except Exception as e:
                print(e)
                print("please re-input")


class RLPlayer(Player):
    def __init__(self, player_id, agent):
        super().__init__(player_id)
        self.agent = agent

    def get_agent_action(self, game):
        return self.agent.select_action(game, self)
