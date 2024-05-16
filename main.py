import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (glClear, GL_COLOR_BUFFER_BIT,
                       GL_DEPTH_BUFFER_BIT, glRotatef,
                       glBegin, glEnd, glVertex3fv, glColor3fv, GL_LINES,
                       glPushMatrix, glPopMatrix, glMatrixMode, glLoadIdentity,
                       GL_PROJECTION, GL_MODELVIEW)
from OpenGL.GLU import gluPerspective, gluLookAt
from loadFile import draw_model, load_obj
import sys
import math


def draw_grid():
    """Draws a simple grid on the XY plane."""
    glColor3fv((1, 0, 0))  # Set grid color to red
    glBegin(GL_LINES)
    for x in range(-20, 21):
        glVertex3fv((x, 20, 0))
        glVertex3fv((x, -20, 0))
    for y in range(-20, 21):
        glVertex3fv((20, y, 0))
        glVertex3fv((-20, y, 0))
    glEnd()
    glColor3fv((1, 1, 1))


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Camera parameters
    zoom = 10
    azimuth = 0
    elevation = 0

    vertices = []
    faces = []
    if file_path:
        vertices, faces = load_obj(file_path)

    angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    zoom -= 1  # Move camera closer to the origin
                elif event.key == pygame.K_DOWN:
                    zoom += 1  # Move camera further from the origin
                elif event.key == pygame.K_w:
                    elevation += 5  # Look up
                elif event.key == pygame.K_s:
                    elevation -= 5  # Look down
                elif event.key == pygame.K_a:
                    azimuth -= 5  # Look left
                elif event.key == pygame.K_d:
                    azimuth += 5  # Look right

        # Ensure elevation is within -90 to 90 degrees to avoid gimbal lock
        elevation = max(-90, min(90, elevation))

        # Convert spherical coordinates to Cartesian coordinates for the camera
        eye_x = zoom * math.cos(math.radians(elevation)) * \
            math.cos(math.radians(azimuth))
        eye_y = zoom * math.cos(math.radians(elevation)) * \
            math.sin(math.radians(azimuth))
        eye_z = zoom * math.sin(math.radians(elevation))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set the perspective projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)

        # Set the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye_x, eye_y, eye_z,  # Eye position (camera)
                  0, 0, 0,             # Look at origin
                  0, 0, 1)             # Up vector (z-axis)

        # Draw the grid
        draw_grid()

        # Apply rotation and draw the model
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)  # Rotate the model around the y-axis
        draw_model(vertices, faces)
        glPopMatrix()

        angle += 1  # Increment the rotation angle

        # Update display
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
