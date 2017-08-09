""" Welcome to the Amazing Adventures of the Courageous Corgi!
This is the first part of his Amazing Adventures, and you're now in the main module.
Run it, and let the Adventures begin!
"""
from cocos.director import director
from cocos.audio.pygame import mixer

from main_menu import new_menu

if __name__ == '__main__':
    director.init(fullscreen=True,
                  caption='The Amazing Adventures of the Courageous Corgi! Part 1')
    mixer.init()
    director.run(new_menu())
