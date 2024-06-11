import math
import pygame


class Camera:
    def __init__(self, zoom=20, azimuth=0, elevation=20, fov=45):
        self.zoom = zoom
        self.azimuth = azimuth
        self.elevation = elevation
        self.fov = fov

    def calculate_eye_x(self):
        return self.zoom * math.cos(math.radians(self.elevation)) * \
            math.cos(math.radians(self.azimuth))

    def calculate_eye_y(self):
        return self.zoom * math.cos(math.radians(self.elevation)) * \
            math.sin(math.radians(self.azimuth))

    def calculate_eye_z(self):
        return self.zoom * math.sin(math.radians(self.elevation))

    def change_camera_position(self, event):
        if event.key == pygame.K_UP:
            self.zoom -= 1  # Move self closer to the origin
        elif event.key == pygame.K_DOWN:
            self.zoom += 1  # Move self further from the origin
        elif event.key == pygame.K_w:
            self.elevation += 5  # Look up
        elif event.key == pygame.K_s:
            self.elevation -= 5  # Look down
        elif event.key == pygame.K_a:
            self.azimuth -= 5  # Look left
        elif event.key == pygame.K_d:
            self.azimuth += 5  # Look right