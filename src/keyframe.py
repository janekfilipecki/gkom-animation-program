from light import Light, Material
from camera import Camera
from load_file import Model

class Keyframe:
    def __init__(self,
                 frame_idx: int,
                 transform_mode: str,
                 translation: list(float),
                 rotation: list(float),
                 scale: list(float),
                 light: Light,
                 material: Material,
                 Model: Model,
                 camera: Camera):
        self.frame_idx = frame_idx
        self.transform_mode = transform_mode
        self.translation = translation
        self.rotation = rotation
        self.scale = scale
        self.light = light
        self.material = material
        self.Model = Model
        self.camera = camera
