import pygame
from config import resource_path


class Som:
    def __init__(self):
        self.musica = pygame.mixer.music
        self.musica.load(resource_path("sounds/musica_fundo.ogg"))
        self.musica.set_volume(1)

    def play(self):
        #self.musica.play()
        ...
    
    def stop(self):
        #self.musica.stop()
        ...
