import math


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