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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
SPRITE_LEVEL_Y_HIGH = 310
LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = "Down"
STOPPED = "Stooped"
MOONWALK = "MonnWalk"