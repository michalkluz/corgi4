from cocos.director import director
from main_menu import new_menu
from cocos.audio.pygame import mixer


if __name__ == '__main__':
    director.init(fullscreen=True,
                  caption='The Amazing Adventures of the Courageous Corgi! Part 1')
    mixer.init()
    director.run(new_menu())

    
    