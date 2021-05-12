import pygame
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def calcule_vetor_distance(center1, center2):
    return pygame.Vector2(center1).distance_to(pygame.Vector2(center2))


def verify_align(y1, y2):
    if y1 in range(y2 - DERIVACAO, y2 + DERIVACAO):
        return True
    else:
        return False


pygame.init()

pygame.display.set_caption('Leo Brooklin Stories')

SCREEN_HEIGHT = pygame.display.Info().current_h
SCREEN_WIDTH = pygame.display.Info().current_w

if pygame.display.get_driver() in ['x11', 'windib', 'directx']:
    flag = pygame.RESIZABLE
    SCREEN_WIDTH = int(SCREEN_WIDTH / 1.5)
    SCREEN_HEIGHT = int(SCREEN_HEIGHT / 1.5)
else:
    flag = pygame.FULLSCREEN

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), flag)

RESIZE_FACTOR = SCREEN_HEIGHT / 600

FONT_SIZE = int(SCREEN_HEIGHT * 0.06)

SPRITE_LEVEL_Y_HIGH = SCREEN_HEIGHT * 0.72
LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = "Down"
STOPPED = "Stooped"
MOONWALK = "MonnWalk"
DERIVACAO = 40
STATE_INATTACK = "In_Attack"
STATE_ATTACK = "Attack"
STATE_STOP = "Stop"
STATE_WALK = "Walk"
STATE_MOONWALK = "MoonWalk"
DIFICULT_AVANCE = 1000
