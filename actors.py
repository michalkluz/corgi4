import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu
from cocos import actions
import pyglet.image as img


class Consumable(cocos.sprite.Sprite):
    """Sprites that the player may pick up, making them disappear
    and increasing the player's jump range
    """

    def __init__(self, position, image):
        super().__init__(image)
        self.position = position
        self.cshape = cm.CircleShape(position, self.width/2)
        self.jump_boost = 20


class Player(cocos.sprite.Sprite):
    """Sprite representing the player
    """

    def __init__(self, position):
        super().__init__('assets/corgi1.png')
        self.position = position
        self.starting_position = position
        self.cshape = cm.AARectShape(position, self.width/6, self.height/12)
        self.update_cshape()
        self.lives = 3
        self.jump_range = 140
        self.speed = 0
        self.max_speed = 3.5
        self.acceleration = 0.15
        self.image_load()
        self.may_jump = True

    def image_load(self):
        """Loads the sprites used for player sprite: standing, jumping, running around.
        """
        self.standing = img.load('assets/corgi1.png')
        self.running = img.load_animation('assets/corgi1.gif')
        self.running.add_to_texture_bin(img.atlas.TextureBin())
        self.jumping = img.load('assets/jump.png')

    def get_speed(self):
        """increases and returns the speed of the player
        """
        if self.speed <= self.max_speed:
            self.speed += self.acceleration
        return self.speed

    def move(self, versor_x, versor_y):
        if self.image != self.running:
            self.image = self.running
        #turns the player left or right
        if versor_x == 1 and self.scale_x != -1:
            self.scale_x = -1
        if versor_x == -1 and self.scale_x != 1:
            self.scale_x = 1
        
        self.x += versor_x * self.get_speed()
        self.y += versor_y * self.get_speed()
        
    def jump(self, versor_x, versor_y):
        self.image = self.jumping
        jump = cocos.actions.JumpBy((self.jump_range * versor_x,
                                            self.jump_range * versor_y), height=30, jumps=1, duration=0.4)
        self.do(jump)


    def stand(self):
        self.image = self.standing
        self.speed = 0


    def update_cshape(self):
        """Updates the collision's center of a player's sprite to be slightly below
        the center of his current position.
        """
        self.cshape.center = eu.Vector2(self.x, self.y - self.height*0.30)

