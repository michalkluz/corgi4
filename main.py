from collections import defaultdict

import cocos
import cocos.collision_model as cm
import cocos.mapcolliders as mc
import cocos.euclid as eu
import cocos.rect as rect

import config as cfg

import pyglet
from pyglet.window import key


class MainLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(MainLayer, self).__init__()
        """ Initializes the world, places background and all actors in the specified positions.
        Builds the collision manager and sets up the starting parameters of the game.

        """
        self.animation = pyglet.image.load_animation('assets/corgi1.gif')
        bin_ = pyglet.image.atlas.TextureBin()
        self.animation.add_to_texture_bin(bin_)
        self.place_sprites()

        # Initializes the collision manager and all starting parameters, sets up the scheduler.
        cell = self.player.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, cfg.WINDOW_WIDTH, 0,
                                               cfg.WINDOW_HEIGHT, cell, cell)

        self.player_speed = PlayerSpeed()
        self.lives = 6000 # cfg.STARTING_LIVES
        self.score = cfg.STARTING_SCORE
        self.may_jump = True
        self.may_walk = True
        self.facing_right = False
        self.jump_range = cfg.JUMP
        self.pressed = defaultdict(int)

        # Starts the main loop of the game
        self.schedule(self.update)

    def place_sprites(self):
        
        for object in game_SpecialLayer.objects:
            if object.name == "STARTINGPOSITION":
                starting_position = object
            if object.name == "FINISHPOSITION":
                self.finish_object = rect.Rect(object.x, object.y, 50, 50)
        # for object in game_DeathLayer.objects:
        #     self.death = rect.Rect(object.x, object.y, 50, 50)
                    
        self.player = Actor(starting_position.position,
                            cfg.PLAYER_STANDING, cfg.PLAYER_SHAPE)
        self.add(self.player)
        self.collision_center = eu.Vector2(self.player.x, self.player.y - self.player.height*0.30)
        self.starting_position = starting_position.position
        self.player.cshape = cm.AARectShape(pos, self.player.width / 6, self.player.height / 12)

        for object in game_Consumable.objects:
            GBone = Consumable(object.position, cfg.GOLDEN_BONE_SPRITE, cfg.GOLDEN_BONE_SHAPE)
            self.add(GBone)
        
    def on_key_press(self, k, m):
        """ Sets up the pressed key to be equal to 1

        """
        self.pressed[k] = 1

    def on_key_release(self, k, m):
        """ Sets up the released key to be equal to 0

        """
        self.pressed[k] = 0

    def update_score(self):
        """ Adds score and checks if the game is over

        """
        self.jump_range += cfg.JUMP_BONUS


    def game_over(self):
        """ Stops the game and displays a game over message

        """
        # Stops the update() loop of the game
        self.pause_scheduler()

        message = Actor(cfg.CENTER_POSITION,
                        cfg.GAME_OVER_MESSAGE, cfg.MESSAGE_SHAPE)
        self.add(message)

    def lose_life(self):
        """ Decrements the number of lives and checks if the game is over. If not, it teleports
        player to the starting position.

        """
        self.lives -= 1
        if self.lives == 0:
            self.game_over()

        self.player.position = self.starting_position
        self.player.cshape.center = eu.Vector2(self.player.x, self.player.y - self.player.height*0.30) 

    def move(self, dt):

        versor_x = self.pressed[key.RIGHT] - self.pressed[key.LEFT]
        versor_y = self.pressed[key.UP] - self.pressed[key.DOWN]
        space_pressed = self.pressed[key.SPACE]
        is_jumping = self.player.are_actions_running()
        is_moving = (versor_x != 0 or versor_y != 0)
        jump_action = cocos.actions.JumpBy((self.jump_range * versor_x,
                                            self.jump_range * versor_y), 30, 1, duration=0.4)

        # if the player is standing still
        if is_jumping is False and is_moving is False:
            self.player.image_change(cfg.PLAYER_STANDING)
            self.player_speed.speed_factor = 0.1
            self.may_walk = True
        # makes the player turn left or right


        # if the player is running
        if is_moving is True:
            if self.may_walk is True and is_jumping is False:
                self.player.image = self.animation
                self.may_walk = False
            self.player_speed.accelerate()
            self.player.scale_x = 1

            player_last = self.player.get_rect()
            player_new = self.player.get_rect()
            if self.facing_right is True or versor_x == 1:
                self.player.scale_x = -1
                self.facing_right = True
            if self.facing_right is False or versor_x == -1:
                self.player.scale_x = 1
                self.facing_right = False

            vx = self.player_speed.get_speed() * versor_x * dt
            vy = self.player_speed.get_speed() * versor_y * dt
 
            player_new.set_x(player_last.x + vx)
            player_new.set_y(player_last.y + vy)

            Collider.collide_map(game_CollisionLayer, player_last, player_new, vx, vy)
            self.player.position = player_new.center

            self.player.cshape.center = eu.Vector2(self.player.x, self.player.y - self.player.height*0.30) 

        # if the player jumps
        if space_pressed == 0:
            self.may_jump = True
        if space_pressed == 1 and is_jumping is False and self.may_jump is True:
            super(Actor, self.player).do(jump_action)
            self.player.image_change(cfg.PLAYER_JUMP)
            self.player.cshape.center = eu.Vector2(self.player.x, self.player.y - self.player.height*0.30) 
            self.may_jump = False
            self.may_walk = True

    def update(self, dt):
        """ Main loop of the game. Checks the player collision with a consumable
        and allows the player to move.

        """
        self.collide()
        self.move(dt)
        self.check_victory()

    def check_victory(self):
        if self.finish_object.contains(self.player.x, self.player.y):
            self.game_over()

    def collide(self):
        """Checks for collisions with the player at the current player's position
        If there's a collision found with a consumable, the consumable is removed
        and the score is updated.

        """
        # clears the memory of the collision manager
        self.collman.clear()

        # adds every object in range of the collision manager
        for _, node in self.children:
            self.collman.add(node)
        for object in game_DeathLayer.objects:
            self.collman.add(object)
        for other in self.collman.iter_colliding(self.player):
            if other.name == "Consumable":
                self.remove(other)
                self.update_score()
            if other.name == "Death":
                self.lose_life()
      

class Actor(cocos.sprite.Sprite):

    def __init__(self, coords, image, shape):
        super().__init__(image)
        pos = self.sprite_position(coords)
        self.collision_shape(shape, pos)

    def sprite_position(self, coords):
        x, y = coords
        self.position = pos = eu.Vector2(x, y)
        return pos

    def collision_shape(self, shape, pos):

        if shape == "box":
            self.cshape = cm.AARectShape(pos, self.width / 2, self.height / 2)
        if shape == "circle":
            self.cshape = cm.CircleShape(pos, self.width / 2)

    def image_change(self, image):
        self.image = pyglet.image.load(image)


class Consumable(Actor):

    def __init__(self, coords, image, shape):
        super().__init__(coords, image, shape)
        self.set_score(image)
        self.name = "Consumable"

    def set_score(self, image):
        if image == cfg.GOLDEN_BONE_SPRITE:
            self.score = cfg.GOLDEN_BONE_SCORE
            self.speed_boost = cfg.GOLDEN_BONE_SPEED_BOOST

        if image == cfg.BONE_SPRITE:
            self.score = cfg.BONE_SCORE
            self.speed_boost = cfg.BONE_SPEED_BOOST


class PlayerSpeed:
    def __init__(self):
        self.acceleration = 0.15
        self.speed_factor = 0.1
        self.speed = cfg.STARTING_SPEED * self.speed_factor

    def get_speed(self):
        return cfg.STARTING_SPEED * self.speed_factor

    def accelerate(self):
        if self.speed_factor < 1:
            self.speed_factor += self.acceleration


if __name__ == '__main__':

    cocos.director.director.init(fullscreen=True,
                                 caption='The Amazing Adventures of the Courageous Corgi! Part 1')

    game_Background = cocos.tiles.load(cfg.MAP_PATH)['Background']
    game_TopLayer = cocos.tiles.load(cfg.MAP_PATH)['TopLayer']
    game_SpecialLayer = cocos.tiles.load(cfg.MAP_PATH)['SpecialLayer']
    game_DeathLayer = cocos.tiles.load(cfg.MAP_PATH)['DeathLayer']
    game_CollisionLayer = cocos.tiles.load(cfg.MAP_PATH)['CollisionLayer']
    Collider = mc.TmxObjectMapCollider(velocity_on_bump="slide")
    game_Consumable = cocos.tiles.load(cfg.MAP_PATH)['Consumable']
    game_DeathLayer.set_view(0, 0, game_TopLayer.px_width, game_TopLayer.px_height)
    scene = cocos.scene.Scene(game_Background)
    for object in game_Consumable.objects:
        pos = eu.Vector2(object.x, object.y)
        object.cshape = cm.CircleShape(pos, object.width)
        object.name = "Consumable"
    for object in game_DeathLayer.objects:
        object.cshape = cm.AARectShape(object.center, object.width*0.5, object.height*0.5)
        object.name = "Death"
        
 
    main_layer = MainLayer()

    
    game_Background.set_view(0, 0, game_Background.px_width, game_Background.px_height)
    scene.add(main_layer)
    scene.add(game_TopLayer)
    game_TopLayer.set_view(0, 0, game_TopLayer.px_width, game_TopLayer.px_height)
    scene.add(game_DeathLayer)
    # scene.add(game_CollisionLayer)
    # scene.add(game_Consumable)
    cocos.director.director.run(scene)
