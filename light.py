from OpenGL.GL import (glEnable, GL_LIGHTING, GL_LIGHT0, GL_AMBIENT,
                       GL_DIFFUSE, GL_SPECULAR, GL_POSITION, GL_FRONT,
                       GL_SHININESS, glMaterialfv, glLightfv, glMaterialf)


class Material:
    def __init__(
            self,
            ambient=[0.2, 0.2, 0.2, 1.0],
            diffuse=[0.8, 0.8, 0.8, 1.0],
            specular=[1.0, 1.0, 1.0, 1.0],
            shininess=50.0
        ):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess


class Light:
    def __init__(
            self,
            material: Material,
            ambient=[0.1, 0.1, 0.1, 1.0],
            diffuse=[0.8, 0.8, 0.8, 1.0],
            specular=[1.0, 1.0, 1.0, 1.0],
            position=[10.0, 10.0, 10.0, 1.0]
        ):
        self.material = material
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.position = position
        self.setup_lighting()

    def change_light(self, ambient=None, diffuse=None, specular=None, position=None):
        if ambient:
            self.ambient = ambient
        if diffuse:
            self.diffuse = diffuse
        if specular:
            self.specular = specular
        if position:
            self.position = position
        self.setup_lighting()

    def setup_lighting(self):
        """Set up lighting for the scene."""
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular)
        glLightfv(GL_LIGHT0, GL_POSITION, self.position)

        glMaterialfv(GL_FRONT, GL_AMBIENT, self.material.ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.material.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.material.specular)
        glMaterialf(GL_FRONT, GL_SHININESS, self.material.shininess)
