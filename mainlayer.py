import cocos.layer
import cocos.collision_model as cm
from cocos.director import director
from pyglet.window import key

import scenario
import actors


class MainLayer(cocos.layer.ScrollableLayer):
    def __init__(self, tile_map, scroller, scenario):
        super(MainLayer, self).__init__()
        self.tile_map = tile_map
        self.place_sprites()
        self.scroller = scroller
        self.scenario = scenario
        cell = self.player.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, self.scenario.background.px_width, 0,
                                               self.scenario.background.px_height, cell, cell)
        self.keys = key.KeyStateHandler()
        director.window.push_handlers(self.keys)
        self.schedule(self.update)

    def place_sprites(self):
        for item in self.tile_map['ItemLayer'].objects:
            if item.name == "Start":
                self.player = actors.Player(item.position)
                self.add(self.player)
            if item.name == "Finish":
                self.finish_position = item.position
            if item.name == "Bone_Normal":
                bone_normal = actors.Consumable(item.position, 'assets/bone_basic_small.png')
                self.add(bone_normal)
            if item.name == "Tree":
                tree = actors.Tree(item.position, 'assets/korona.png')
                self.add(tree)

    def update(self, dt):

        if self.player.are_actions_running() is False:
            self.movement()
        self.player.update_cshape()
        self.collide()
        self.scroller.set_focus(self.player.x, self.player.y)

    def collide(self):
        self.collman.clear()
        for _, node in self.children:
            self.collman.add(node)
        for item in self.collman.iter_colliding(self.player):
            if item.name == "Consumable":
                self.remove(item)
            if item.name == "Tree":
                self.player.stop()

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

