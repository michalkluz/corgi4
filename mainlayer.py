from collections import defaultdict

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
        if self.player.able_to_move:
            self.movement()


    def movement(self):        

        if self.keys[key.SPACE]:
            self.prejump_x, self.prejump_y = self.player.position
            self.player.jump()
        elif (self.keys[key.RIGHT] is not self.keys[key.LEFT]) and (self.player.image is not self.player.running):
            self.player.move()
        else:
            self.player.stand()
        
        if self.keys[key.ENTER]:
            self.player.stop()
            self.player.do(actions.JumpBy((0, self.prejump_y - self.player.y), 0, 1, duration=0.15))
        

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
