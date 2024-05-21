import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       glRotatef, glBegin, glEnd, glVertex3fv, glColor3fv,
                       GL_LINES, glPushMatrix, glPopMatrix, glMatrixMode,
                       glLoadIdentity, GL_PROJECTION, GL_MODELVIEW, glEnable,
                       GL_DEPTH_TEST, GL_LIGHTING, GL_LIGHT0, GL_AMBIENT,
                       GL_DIFFUSE, GL_SPECULAR, GL_POSITION, GL_FRONT,
                       GL_SHININESS, glMaterialfv, glLightfv, glMaterialf,
                       glDisable, glTranslatef, glScalef)
from OpenGL.GLU import gluPerspective, gluLookAt
from loadFile import draw_model, load_obj
import sys
import math
import signal
import tkinter as tk
import threading
import os


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


def pygame_thread(camera_mode, frame_slider, transform_mode):
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Set up the signal handler for graceful exit
    #signal.signal(signal.SIGINT, handle_exit)

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
    translate = [0, 0, 0]
    rotate = [0, 0, 0]
    scale = [1, 1, 1]

    grid = True
    running =  True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                            # Translacja
                if transform_mode.get() == "Translation":
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        translate[0] += 0.1  # Przesunięcie w osi X
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        translate[1] += 0.1  # Przesunięcie w osi Y
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        translate[2] += 0.1  # Przesunięcie w osi Z

                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        translate[0] -= 0.1  # Przesunięcie w osi X w przeciwną stronę
                    elif event.key in (pygame.K_5, pygame.K_KP5):
                        translate[1] -= 0.1  # Przesunięcie w osi Y w przeciwną stronę
                    elif event.key in (pygame.K_6, pygame.K_KP6):
                        translate[2] -= 0.1  # Przesunięcie w osi Z w przeciwną stronę
                # Rotacja
                elif transform_mode.get() == "Rotation":
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        rotate[0] += 5  # Przesunięcie w osi X
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        rotate[1] += 5  # Przesunięcie w osi Y
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        rotate[2] += 5  # Przesunięcie w osi Z

                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        rotate[0] -= 5  # Przesunięcie w osi X w przeciwną stronę
                    elif event.key in (pygame.K_5, pygame.K_KP5):
                        rotate[1] -= 5  # Przesunięcie w osi Y w przeciwną stronę
                    elif event.key in (pygame.K_6, pygame.K_KP6):
                        rotate[2] -= 5  # Przesunięcie w osi Z w przeciwną stronę
                # Skalowanie
                elif transform_mode.get() == "Scaling":
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        scale[0] += 1  # Przesunięcie w osi X
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        scale[1] += 1  # Przesunięcie w osi Y
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        scale[2] += 1  # Przesunięcie w osi Z

                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        scale[0] -= 0.1  # Przesunięcie w osi X w przeciwną stronę
                    elif event.key in (pygame.K_5, pygame.K_KP5):
                        scale[1] -= 0.1  # Przesunięcie w osi Y w przeciwną stronę
                    elif event.key in (pygame.K_6, pygame.K_KP6):
                        scale[2] -= 0.1  # Przesunięcie w osi Z w przeciwną stronę

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

        setup_lighting()

        # Set the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if camera_mode.get() == "Orbiting":
            gluLookAt(eye_x, eye_y, eye_z,  # Eye position (camera)
                      0, 0, 0,             # Look at origin
                      0, 0, 1)             # Up vector (z-axis)
        else:
            gluLookAt(eye_x, eye_y, eye_z,  # Eye position (camera)
                      eye_x + math.cos(math.radians(azimuth)),  # Look at direction
                      eye_y + math.sin(math.radians(azimuth)),
                      eye_z,             # Up vector (z-axis)
                      0, 0, 1)             # Up vector (z-axis)         # Up vector (z-axis)

        # Draw the grid
        if grid:
            draw_grid(zoom, fov, display[0] / display[1])

        # Apply rotation and draw the model
        glPushMatrix()
        glTranslatef(*translate)
        glRotatef(rotate[0], 1, 0, 0)
        glRotatef(rotate[1], 0, 1, 0)
        glRotatef(rotate[2], 0, 0, 1)
        glScalef(*scale)
        draw_model(vertices, faces, normals)
        glPopMatrix()

        angle += 5  # Increment the rotation angle

        # Update display
        pygame.display.flip()
        pygame.time.wait(10)

def show_keyframe_options(keyframe_frame, keyframe_mode, interpolation_mode):
    keyframe_frame.grid(row=3, column=0, columnspan=2, pady=10)
    keyframe_mode.set("Translation")
    interpolation_mode.set("Constant")

def hide_keyframe_options(keyframe_frame):
    keyframe_frame.pack_forget()

def create_gui():
    root = tk.Tk()
    root.title("Kontrolki Animacji")

    # Ustawienia układu głównego okna
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Wbudowanie okna Pygame w okno tkinter
    embed = tk.Frame(root, width=800, height=600)
    embed.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    control_frame = tk.Frame(root)
    control_frame.grid(row=1, column=0, columnspan=2, pady=20)

    camera_mode = tk.StringVar(value="Orbiting")
    tk.Button(control_frame, text="Przełącz Kamerę", command=lambda: camera_mode.set("Freeflight" if camera_mode.get() == "Orbiting" else "Orbiting")).grid(row=0, column=0, pady=5)

    frame_slider = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Klatki")
    frame_slider.grid(row=1, column=0, pady=5)

    keyframe_mode = tk.StringVar()
    interpolation_mode = tk.StringVar()
    transform_mode = tk.StringVar(value="Translation")

    keyframe_frame = tk.Frame(control_frame)
    tk.Label(keyframe_frame, text="Wybierz tryb przekształcenia:").grid(row=0, column=0, pady=5)
    tk.Radiobutton(keyframe_frame, text="Translacja", variable=transform_mode, value="Translation").grid(row=1, column=0, sticky=tk.W, pady=2)
    tk.Radiobutton(keyframe_frame, text="Rotacja", variable=transform_mode, value="Rotation").grid(row=2, column=0, sticky=tk.W, pady=2)
    tk.Radiobutton(keyframe_frame, text="Skalowanie", variable=transform_mode, value="Scaling").grid(row=3, column=0, sticky=tk.W, pady=2)

    tk.Label(keyframe_frame, text="Wybierz interpolację:").grid(row=4, column=0, pady=5)
    tk.Radiobutton(keyframe_frame, text="Stała", variable=interpolation_mode, value="Constant").grid(row=5, column=0, sticky=tk.W, pady=2)
    tk.Radiobutton(keyframe_frame, text="Liniowa", variable=interpolation_mode, value="Linear").grid(row=6, column=0, sticky=tk.W, pady=2)

    tk.Button(keyframe_frame, text="Save", command=lambda: hide_keyframe_options(keyframe_frame)).grid(row=7, column=0, sticky=tk.W, padx=5, pady=10)
    tk.Button(keyframe_frame, text="Odrzuć", command=lambda: hide_keyframe_options(keyframe_frame)).grid(row=7, column=1, sticky=tk.E, padx=5, pady=10)

    tk.Button(control_frame, text="Wstaw Klatkę Kluczową", command=lambda: show_keyframe_options(keyframe_frame, keyframe_mode, interpolation_mode)).grid(row=2, column=0, pady=10)

    def start_pygame():
        threading.Thread(target=pygame_thread, args=(camera_mode, frame_slider, transform_mode), daemon=True).start()

    root.after(100, start_pygame)

    root.mainloop()

if __name__ == "__main__":
    create_gui()