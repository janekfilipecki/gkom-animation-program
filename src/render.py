import imageio
import os
import numpy as np
from OpenGL.GL import (glPixelStorei, GL_PACK_ALIGNMENT, glReadPixels,
                       GL_RGB, GL_UNSIGNED_BYTE)
from PIL import Image


def save_frame(filename):
    directory = os.path.dirname(filename)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, 800, 600, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (800, 600), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    image.save(filename)
    return image


def save_video(frames, filename="animation.mp4"):
    writer = imageio.get_writer(filename, format='mp4', mode='I', fps=20)
    for frame in frames:
        writer.append_data(np.asarray(frame))
    writer.close()
