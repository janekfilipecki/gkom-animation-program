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
import signal


def draw_grid(zoom, fov, aspect):
    """Draws a simple grid on the XY plane, adaptive to the view range."""
    glColor3fv((1, 0, 0))  # Set grid color to red

    # Calculate the visible range at the zoom level
    height = 2 * zoom * math.tan(math.radians(fov) / 2)
    width = height * aspect

    # Adjust grid size to cover the view
    grid_size = max(width, height)

    # Draw the grid
    glBegin(GL_LINES)
    step = 1  # Distance between grid lines
    for x in range(int(-grid_size // 2), int(grid_size // 2) + 1, step):
        glVertex3fv((x, grid_size // 2, 0))
        glVertex3fv((x, -grid_size // 2, 0))
    for y in range(int(-grid_size // 2), int(grid_size // 2) + 1, step):
        glVertex3fv((grid_size // 2, y, 0))
        glVertex3fv((-grid_size // 2, y, 0))
    glEnd()
    glColor3fv((1, 1, 1))  # Reset color to white


def handle_exit(signal, frame):
    pygame.quit()
    sys.exit(0)


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Set up the signal handler for graceful exit
    signal.signal(signal.SIGINT, handle_exit)

    # Camera parameters
    zoom = 10
    azimuth = 0
    elevation = 0
    fov = 45

    vertices = []
    faces = []
    if file_path:
        vertices, faces = load_obj(file_path)

    angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_exit(None, None)
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
        gluPerspective(fov, (display[0] / display[1]), 0.1, 100.0)

        # Set the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye_x, eye_y, eye_z,  # Eye position (camera)
                  0, 0, 0,             # Look at origin
                  0, 0, 1)             # Up vector (z-axis)

        # Draw the grid
        draw_grid(zoom, fov, display[0] / display[1])

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
