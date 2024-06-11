import copy
import pygame
from src.light import Light, Material
from src.camera import Camera
from src.load_file import Model

class Keyframe:
    def __init__(self,
                 frame_idx: int,
                 interpolation_mode: str,
                 translation: list,
                 rotation: list,
                 scale: list):
        self.frame_idx = frame_idx
        self.interpolation_mode = interpolation_mode
        self.translation = copy.deepcopy(translation)
        self.rotation = copy.deepcopy(rotation)
        self.scale = copy.deepcopy(scale)

    def __str__(self):
        return f"frame {self.frame_idx}: {self.interpolation_mode}, {self.translation}, {self.rotation}, {self.scale}"

    def change_translation(self, event):
        if event.key in (pygame.K_1, pygame.K_KP1):
            self.translation[0] += 0.1  # Przesunięcie w osi X
        elif event.key in (pygame.K_2, pygame.K_KP2):
            self.translation[1] += 0.1  # Przesunięcie w osi Y
        elif event.key in (pygame.K_3, pygame.K_KP3):
            self.translation[2] += 0.1  # Przesunięcie w osi Z

        elif event.key in (pygame.K_4, pygame.K_KP4):
            # Przesunięcie w osi X w przeciwną stronę
            self.translation[0] -= 0.1
        elif event.key in (pygame.K_5, pygame.K_KP5):
            # Przesunięcie w osi Y w przeciwną stronę
            self.translation[1] -= 0.1
        elif event.key in (pygame.K_6, pygame.K_KP6):
            # Przesunięcie w osi Z w przeciwną stronę
            self.translation[2] -= 0.1

    def change_rotation(self, event):
        if event.key in (pygame.K_1, pygame.K_KP1):
            self.rotation[0] += 5  # Obrót wokół osi X
        elif event.key in (pygame.K_2, pygame.K_KP2):
            self.rotation[1] += 5  # Obrót wokół osi Y
        elif event.key in (pygame.K_3, pygame.K_KP3):
            self.rotation[2] += 5  # Obrót wokół osi Z

        elif event.key in (pygame.K_4, pygame.K_KP4):
            self.rotation[0] -= 5  # Obrót wokół osi X w przeciwną stronę
        elif event.key in (pygame.K_5, pygame.K_KP5):
            self.rotation[1] -= 5  # Obrót wokół osi Y w przeciwną stronę
        elif event.key in (pygame.K_6, pygame.K_KP6):
            self.rotation[2] -= 5  # Obrót wokół osi Z w przeciwną stronę

    def change_scale(self, event):
        if event.key in (pygame.K_1, pygame.K_KP1):
            self.scale[0] += 1  # Skalowanie w osi X
        elif event.key in (pygame.K_2, pygame.K_KP2):
            self.scale[1] += 1  # Skalowanie w osi Y
        elif event.key in (pygame.K_3, pygame.K_KP3):
            self.scale[2] += 1  # Skalowanie w osi Z

        elif event.key in (pygame.K_4, pygame.K_KP4):
            # Skalowanie w osi X w przeciwną stronę
            self.scale[0] -= 0.1
        elif event.key in (pygame.K_5, pygame.K_KP5):
            # Skalowanie w osi Y w przeciwną stronę
            self.scale[1] -= 0.1
        elif event.key in (pygame.K_6, pygame.K_KP6):
            # Skalowanie w osi Z w przeciwną stronę
            self.scale[2] -= 0.1
