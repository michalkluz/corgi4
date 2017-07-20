import cocos.scene
import cocos.tiles
import cocos.layer

import mainlayer

def load_tilemap(path):
    return cocos.tiles.load(path)

def new_game():
    tile_map = load_tilemap('assets/map1.tmx')
    scenario = Scenario(tile_map)
    gamelayer = mainlayer.MainLayer(tile_map)
    return cocos.scene.Scene(scenario.background, gamelayer, scenario.top)

class Scenario:
    def __init__(self, tile_map):
        self.tile_map = tile_map
        self.background, self.top = self.create_layers()
        
    def create_layers(self):
        background = self.tile_map['Background']
        background.set_view(0, 0, background.px_width, background.px_height)
        top = self.tile_map['TopLayer']
        top.set_view(0, 0, top.px_width, top.px_height)
        return background, top