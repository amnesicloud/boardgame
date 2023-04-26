class Factory:
    def __init__(self, factory_id):
        self.tiles = []
        self.factory_id = factory_id
        self.center = False

    def add_tile(self, tile):
        self.tiles.append(tile)

    # def remove_tile(self, tile):
    #     self.tiles.remove(tile)

    def remove_all_tiles(self):
        print("factory tiles")
        print(self.tiles)
        print(len(self.tiles))
        remaining_tiles = []
        for tile in self.tiles:
            remaining_tiles.append(tile)
        self.tiles = []
        return remaining_tiles

    def is_empty(self):
        return not self.tiles

    def take_tiles(self, color):
        tiles_taken = [tile for tile in self.tiles if tile == color]
        self.tiles = [tile for tile in self.tiles if tile != color]
        return tiles_taken

    def is_center(self):
        return self.center

    def to_dict(self):
        return {
            'tiles': self.tiles,
        }

class Center(Factory):
    def __init__(self):
        super().__init__("center")
        self.center = True

    def add_tile(self, remaining_tiles):
        self.tiles.extend(remaining_tiles)