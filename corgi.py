from cocos.director import director
from main_menu import new_menu


if __name__ == '__main__':
    director.init(fullscreen=True,
                  caption='The Amazing Adventures of the Courageous Corgi! Part 1')
    director.run(new_menu())
    
    