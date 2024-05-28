from PIL import Image
from OpenGL.GL import glPixelStorei, GL_PACK_ALIGNMENT, glReadPixels, GL_RGB, GL_UNSIGNED_BYTE
from OpenGL.GLUT import glutSwapBuffers

width = 800
height = 600


def render(filename="aaa.png"):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL's origin is at the bottom left corner
    image.save(filename)
    print(f"Frame saved as {filename}")