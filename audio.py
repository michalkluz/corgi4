from cocos.layer import Layer
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

class Audio(Sound):
    def __init__(self, file_path):
        super(Audio, self).__init__(file_path)

class AudioLayer(Layer):
    def __init__(self):
        super(AudioLayer, self).__init__()
        song = Audio("assets/epicmusic.ogg")
        song.play(-1)