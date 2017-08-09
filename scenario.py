import cocos.scene
import cocos.tiles
import cocos.layer
import mainlayer
import audio

def load_tilemap(path):
    return cocos.tiles.load(path)

def new_game():
    tile_map = load_tilemap('assets/map1.tmx')
    scenario = Scenario(tile_map)
    scroller = cocos.layer.ScrollingManager()
    gamelayer = mainlayer.MainLayer(tile_map, scroller, scenario)

    scroller.add(scenario.background)
    musiclayer = audio.AudioLayer()
    scroller.add(gamelayer)
    return cocos.scene.Scene(scroller, musiclayer)


class Scenario:
    def __init__(self, tile_map):
        self.tile_map = tile_map
        self.background = self.create_layers()
        
    def create_layers(self):
        background = self.tile_map['Background']
        return background #top