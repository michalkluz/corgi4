import cocos.scene
import cocos.menu
from cocos.scenes.transitions import FadeTransition
from cocos.director import director
import pyglet.app
from scenario import new_game


class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__(
            'The Amazing Adventures of the Courageous Corgi! Part 1')

        menu_items = list()
        menu_items.append(cocos.menu.MenuItem('Begin a new Adventure!', self.on_new_game))
        menu_items.append(cocos.menu.MenuItem('Quit', pyglet.app.exit))
        self.create_menu(menu_items)

    def on_new_game(self):
        director.push(FadeTransition(new_game(), duration=2))
        


def new_menu():
    """ Creates a cocos scene.
    Returns scene object for the corgi.py's director.run function
    """
    scene = cocos.scene.Scene()
    scene.add(MainMenu())
    return scene

# def on_new_game(self):
#     director.push(FadeTRTransition(new_game(), duration=2))
 # menu_items.append(cocos.menu.ToggleMenuItem('Show FPS: ', self.show_fps, director.show_FPS))
# import cocos.layer
# import cocos.actions as ac
# from cocos.director import director
# from cocos.scenes.transitions import FadeTRTransition
# from gamelayer import new_game

#         self.font_title['font_name'] = 'Oswald'
#         self.font_item['font_name'] = 'Oswald'
#         self.font_item_selected['font_name'] = 'Oswald'

#         self.menu_anchor_y = 'center'
#         self.menu_anchor_x = 'center'

    # self.create_menu(items, ac.ScaleTo(1.25, duration=0.25), ac.ScaleTo(1.0, duration=0.25))

#     def on_new_game(self):
#         director.push(FadeTRTransition(new_game(), duration=2))

#     def show_fps(self, val):
#         director.show_FPS = val
