import cocos.layer
import cocos.collision_model as cm
from cocos.director import director
from cocos import actions
from pyglet.window import key

import actors


class MainLayer(cocos.layer.Layer):
    def __init__(self, tile_map):
        super(MainLayer, self).__init__()
        self.tile_map = tile_map
        self.place_sprites()
        cell = self.player.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, director.window.width, 0, director.window.height, cell, cell)
        self.keys = key.KeyStateHandler()
        director.window.push_handlers(self.keys)
        self.schedule(self.update)

    def update(self, dt):
        if self.player.are_actions_running() is False:
            self.movement()

    def movement(self):        
        versor_x = int(self.keys[key.RIGHT]) - int(self.keys[key.LEFT])
        versor_y = int(self.keys[key.UP]) - int(self.keys[key.DOWN])

        if self.keys[key.SPACE]:
            self.player.jump(versor_x, versor_y)
        elif versor_x != 0 or versor_y != 0:
            self.player.move(versor_x, versor_y)
        else:
            self.player.stand()
        

    def place_sprites(self):
        for consumable in self.tile_map['Consumable'].objects:
            golden_bone = actors.Consumable(
                consumable.position, 'assets/goldenbone1.png')
            golden_bone.name = "Consumable"
            self.add(golden_bone)

        for special in self.tile_map['SpecialLayer'].objects:
            if special.name == "STARTINGPOSITION":
                self.player = actors.Player(special.position)
                self.add(self.player)
            if special.name == "FINISHPOSITION":
               self.finish_position = special.position
