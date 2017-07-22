import cocos.layer
import cocos.collision_model as cm
from cocos.director import director
from cocos import actions
from pyglet.window import key

import actors
import scenario


class MainLayer(cocos.layer.ScrollableLayer):
    def __init__(self, tile_map, scroller):
        super(MainLayer, self).__init__()
        self.tile_map = tile_map
        self.place_sprites()
        self.scroller = scroller
        cell = self.player.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, director.window.width, 0, director.window.height, cell, cell)
        self.keys = key.KeyStateHandler()
        director.window.push_handlers(self.keys)
        self.schedule(self.update)

    def update(self, dt):
        if self.player.are_actions_running() is False:
            self.movement()
        self.scroller.set_focus(self.player.x, self.player.y)
   
    def movement(self):        
        versor_x = int(self.keys[key.RIGHT]) - int(self.keys[key.LEFT])
        versor_y = int(self.keys[key.UP]) - int(self.keys[key.DOWN])
        if self.keys[key.SPACE] is False:
            self.player.may_jump = True

        if self.keys[key.SPACE] and self.player.may_jump:
            self.player.jump(versor_x, versor_y)
            self.player.may_jump = False
        elif versor_x != 0 or versor_y != 0:
            self.player.move(versor_x, versor_y)
        else:
            self.player.stand()

        

    def place_sprites(self):
        # for consumable in self.tile_map['Consumable'].objects:
        #     golden_bone = actors.Consumable(
        #         consumable.position, 'assets/goldenbone1.png')
        #     golden_bone.name = "Consumable"
        #     self.add(golden_bone)

        for special in self.tile_map['SpecialLayer'].objects:
            if special.name == "STARTINGPOSITION":
                self.player = actors.Player(special.position)
                self.add(self.player)
            if special.name == "FINISHPOSITION":
               self.finish_position = special.position
