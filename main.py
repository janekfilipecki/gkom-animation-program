import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       glRotatef, glBegin, glEnd, glVertex3fv, glColor3fv,
                       GL_LINES, glPushMatrix, glPopMatrix, glMatrixMode,
                       glLoadIdentity, GL_PROJECTION, GL_MODELVIEW, glEnable,
                       GL_DEPTH_TEST, GL_LIGHTING, GL_LIGHT0, GL_AMBIENT,
                       GL_DIFFUSE, GL_SPECULAR, GL_POSITION, GL_FRONT,
                       GL_SHININESS, glMaterialfv, glLightfv, glMaterialf,
                       glDisable)
from OpenGL.GLU import gluPerspective, gluLookAt
from loadFile import draw_model, load_obj
import sys
import math
import signal


def draw_grid(zoom, fov, aspect):
    """Draws a simple grid on the XY plane, adaptive to the view range."""
    glDisable(GL_LIGHTING)  # Disable lighting to ensure
    # the grid color is not affected

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

    glEnable(GL_LIGHTING)  # Re-enable lighting after drawing the grid
    glColor3fv((1, 1, 1))  # Reset color to white


def handle_exit(signal, frame):
    pygame.quit()
    sys.exit(0)


def setup_lighting():
    """Set up lighting for the scene."""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Define light properties
    light_ambient = [0.1, 0.1, 0.1, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [10.0, 10.0, 10.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # Define material properties
    material_ambient = [0.2, 0.2, 0.2, 1.0]
    material_diffuse = [0.8, 0.8, 0.8, 1.0]
    material_specular = [1.0, 1.0, 1.0, 1.0]
    material_shininess = 50.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, material_shininess)


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Set up the signal handler for graceful exit
    signal.signal(signal.SIGINT, handle_exit)

    # Set up lighting
    setup_lighting()

    near_render_distance = 0.1
    far_render_distance = 1000

    # Camera parameters
    zoom = 20  # Initial zoom distance
    azimuth = 0  # Initial azimuth angle
    elevation = 20  # Initial elevation angle
    fov = 45  # Field of view

    vertices = []
    faces = []
    normals = []
    if file_path:
        vertices, faces, normals = load_obj(file_path)

    angle = 0

    grid = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_exit(None, None)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    grid = not grid
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
        gluPerspective(fov, (display[0] / display[1]),
                       near_render_distance, far_render_distance)

        # Set the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye_x, eye_y, eye_z,  # Eye position (camera)
                  0, 0, 0,             # Look at origin
                  0, 0, 1)             # Up vector (z-axis)

        # Draw the grid
        if grid:
            draw_grid(zoom, fov, display[0] / display[1])

        # Apply rotation and draw the model
        glPushMatrix()
        glRotatef(angle, 1, 1, 1)  # Rotate the model around the y-axis
        draw_model(vertices, faces, normals)
        glPopMatrix()

        angle += 5  # Increment the rotation angle

        # Update display
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
