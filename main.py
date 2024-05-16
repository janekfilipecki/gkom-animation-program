import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT
from OpenGL.GL import (glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       glBegin, glEnd, glVertex3fv, GL_TRIANGLES, glTranslatef,
                       glRotatef)
from OpenGL.GLU import gluPerspective
from loadFile import draw_model, load_obj
import sys
import tkinter as tk
from tkinter import filedialog


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    vertices = []
    faces = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:  # Press 'L' key to load a new model
                    root = tk.Tk()
                    root.withdraw()
                    file_path = filedialog.askopenfilename(filetypes=[("OBJ Files", "*.obj")])
                    if file_path:
                        vertices, faces = load_obj(file_path)

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_model(vertices, faces)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
