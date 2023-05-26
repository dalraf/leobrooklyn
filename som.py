import pygame
from config import resource_path


class Som:
    def __init__(self):
        self.musica = pygame.mixer.music
        self.musica.load(resource_path("sounds/musica_fundo.ogg"))

    def play(self):
        self.musica.play()
    
    def stop(self):
        self.musica.stop()
