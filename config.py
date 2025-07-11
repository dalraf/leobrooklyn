import pygame
import sys
import os


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def calcule_vetor_distance(center1, center2):
    return pygame.Vector2(center1).distance_to(pygame.Vector2(center2))


def verify_align(y1: int, y2: int) -> bool:
    """Verifica se duas coordenadas Y estão alinhadas dentro da margem DERIVACAO"""
    return abs(y1 - y2) <= DERIVACAO


pygame.init()

pygame.display.set_caption("Leo Brooklin Stories")

#SCREEN_HEIGHT = pygame.display.Info().current_h
#SCREEN_WIDTH = pygame.display.Info().current_w
#print(SCREEN_HEIGHT)
#print(SCREEN_WIDTH)

# if pygame.display.get_driver() in ["x11", "windib", "directx"]:
#flag = pygame.RESIZABLE
#SCREEN_WIDTH = int(SCREEN_WIDTH / 1.5)
#SCREEN_HEIGHT = int(SCREEN_HEIGHT / 1.5)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# else:
#     flag = pygame.FULLSCREEN

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RESIZE_FACTOR = SCREEN_HEIGHT / 600

FONT_SIZE = int(SCREEN_HEIGHT * 0.06)

SPRITE_LEVEL_Y_HIGH = SCREEN_HEIGHT * 0.70
LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = "Down"
STOPPED = "Stopped"
MOONWALK = "MoonWalk"
DERIVACAO = 40
STATE_INATTACK = "In_Attack"
STATE_ATTACK = "Attack"
STATE_STOP = "Stop"
STATE_WALK = "Walk"
STATE_MOONWALK = "MoonWalk"
DIFICULT_AVANCE = 1000

# Constantes adicionadas do TODO.md
ENEMY_SPAWN_TICK_RESET = 100
PARALLAX_START_THRESHOLD = 0.8
WHITE_COLOR = (255, 255, 255)
GAME_FPS = 40

# Constantes para UI de botões
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 40
DPAD_BUTTON_SIZE = 50
DPAD_PADDING = 10
ACTION_BUTTON_SIZE = 60
ACTION_BUTTON_PADDING = 20
UI_BOTTOM_MARGIN = 10
