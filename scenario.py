import cocos.scene
import cocos.tiles
import cocos.layer
from cocos.director import director
import mainlayer
import audio

def load_tilemap(path):
    return cocos.tiles.load(path)

def new_game():
    tile_map = load_tilemap('assets/map.tmx')
    scenario = Scenario(tile_map)
    scroller = cocos.layer.ScrollingManager()
    gamelayer = mainlayer.MainLayer(tile_map, scroller)

    scroller.add(scenario.background)
    musiclayer = audio.AudioLayer()
    scroller.add(gamelayer)

    #scroller.add(scenario.top)
    return cocos.scene.Scene(scroller, musiclayer)


class Scenario:
    def __init__(self, tile_map):
        self.tile_map = tile_map
        self.background = self.create_layers()
        
    def create_layers(self):
        background = self.tile_map['background']
       # top = self.tile_map['TopLayer']
       # top.set_view(0, 0, top.px_width, top.px_height)
        return background #top