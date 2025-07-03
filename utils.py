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


def verify_align(y1: int, y2: int, derivacao: int) -> bool:
    """Verifica se duas coordenadas Y estão alinhadas dentro da margem DERIVACAO"""
    return abs(y1 - y2) <= derivacao
