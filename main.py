import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       glRotatef, glBegin, glEnd, glVertex3fv, glColor3fv,
                       GL_LINES, glPushMatrix, glPopMatrix, glMatrixMode,
                       glLoadIdentity, GL_PROJECTION, GL_MODELVIEW, glEnable,
                       GL_DEPTH_TEST, GL_LIGHTING, glDisable, glTranslatef, glScalef)
from OpenGL.GLU import gluPerspective, gluLookAt
from gui.control_frame import create_control_frame
from gui.light_frame import create_light_frame
from gui.material_frame import create_material_frame
from gui.render_frame import create_render_frame
from gui.utils import get_coordinates, get_shininess, choose_color, save_keyframe
from src.load_file import draw_model, load_obj
from src.light import Light, Material
import sys
import math
import signal
import tkinter as tk
from tkinter import ttk
import threading
from src.render import render

keyframes = []
interpolation_mode = None
translate = [0, 0, 0]
rotate = [0, 0, 0]
scale = [1, 1, 1]


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


def interpolate(start, end, alpha, mode):
    if mode == "Linear":
        return start + (end - start) * alpha
    return start


def apply_transformations(transform, alpha, mode):
    translate = [interpolate(transform[0][i], transform[1]
                             [i], alpha, mode) for i in range(3)]
    rotate = [interpolate(transform[2][i], transform[3]
                          [i], alpha, mode) for i in range(3)]
    scale = [interpolate(transform[4][i], transform[5][i],
                         alpha, mode) for i in range(3)]

    glTranslatef(*translate)
    glRotatef(rotate[0], 1, 0, 0)
    glRotatef(rotate[1], 0, 1, 0)
    glRotatef(rotate[2], 0, 0, 1)
    glScalef(*scale)


def update_transformations(frame_slider, transform_mode):
    global keyframes, interpolation_mode, translate, rotate, scale

    if not keyframes:
        return translate, rotate, scale

    current_frame = frame_slider.get()
    prev_keyframe = None
    next_keyframe = None

    for i, keyframe in enumerate(keyframes):
        frame, _, _, _ = keyframe
        if frame <= current_frame:
            prev_keyframe = keyframe
        if frame >= current_frame and next_keyframe is None:
            next_keyframe = keyframe
            break

    # Jeśli nie ma poprzedniej klatki kluczowej, użyj pierwszej klatki kluczowej
    if prev_keyframe is None:
        prev_keyframe = keyframes[0]

    # Jeśli nie ma następnej klatki kluczowej, użyj ostatniej klatki kluczowej
    if next_keyframe is None:
        next_keyframe = keyframes[-1]

    start_frame, start_translate, start_rotate, start_scale = prev_keyframe
    end_frame, end_translate, end_rotate, end_scale = next_keyframe

    if start_frame == end_frame:
        return start_translate, start_rotate, start_scale

    alpha = (current_frame - start_frame) / (end_frame - start_frame)
    translate = [interpolate(start_translate[i], end_translate[i],
                             alpha, transform_mode.get()) for i in range(3)]
    rotate = [interpolate(start_rotate[i], end_rotate[i],
                          alpha, transform_mode.get()) for i in range(3)]
    scale = [interpolate(start_scale[i], end_scale[i], alpha,
                         transform_mode.get()) for i in range(3)]

    return translate, rotate, scale


def pygame_thread(frame_slider, transform_mode):
    global keyframes, interpolation_mode, translate, rotate, scale, material, light

    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Set up the signal handler for graceful exit
    # signal.signal(signal.SIGINT, handle_exit)

    # Set up lighting
    material = Material()
    light = Light(material)

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
    running = True
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
                elif event.key == pygame.K_p:  # Save frame when 'P' is pressed
                    render()
                # Translacja
                if transform_mode.get() == "Translation":
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        translate[0] += 0.1  # Przesunięcie w osi X
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        translate[1] += 0.1  # Przesunięcie w osi Y
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        translate[2] += 0.1  # Przesunięcie w osi Z

                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        # Przesunięcie w osi X w przeciwną stronę
                        translate[0] -= 0.1
                    elif event.key in (pygame.K_5, pygame.K_KP5):
                        # Przesunięcie w osi Y w przeciwną stronę
                        translate[1] -= 0.1
                    elif event.key in (pygame.K_6, pygame.K_KP6):
                        # Przesunięcie w osi Z w przeciwną stronę
                        translate[2] -= 0.1
                # Rotacja
                elif transform_mode.get() == "Rotation":
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        rotate[0] += 5  # Obrót wokół osi X
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        rotate[1] += 5  # Obrót wokół osi Y
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        rotate[2] += 5  # Obrót wokół osi Z

                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        rotate[0] -= 5  # Obrót wokół osi X w przeciwną stronę
                    elif event.key in (pygame.K_5, pygame.K_KP5):
                        rotate[1] -= 5  # Obrót wokół osi Y w przeciwną stronę
                    elif event.key in (pygame.K_6, pygame.K_KP6):
                        rotate[2] -= 5  # Obrót wokół osi Z w przeciwną stronę
                # Skalowanie
                elif transform_mode.get() == "Scaling":
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        scale[0] += 1  # Skalowanie w osi X
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        scale[1] += 1  # Skalowanie w osi Y
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        scale[2] += 1  # Skalowanie w osi Z

                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        # Skalowanie w osi X w przeciwną stronę
                        scale[0] -= 0.1
                    elif event.key in (pygame.K_5, pygame.K_KP5):
                        # Skalowanie w osi Y w przeciwną stronę
                        scale[1] -= 0.1
                    elif event.key in (pygame.K_6, pygame.K_KP6):
                        # Skalowanie w osi Z w przeciwną stronę
                        scale[2] -= 0.1

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

        light.setup_lighting()

        # Set the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye_x, eye_y, eye_z,  # Eye position (camera)
                  0, 0, 0,             # Look at origin
                  0, 0, 1)             # Up vector (z-axis)

        # Draw the grid
        if grid:
            draw_grid(zoom, fov, display[0] / display[1])

        # Apply transformations and draw the model
        glPushMatrix()
        if keyframes:
            translate, rotate, scale = update_transformations(
                frame_slider, transform_mode)
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


def save_keyframe_handler(frame_slider, keyframe_listbox):
    save_keyframe(frame_slider, keyframe_listbox, keyframes, translate, rotate, scale)


def light_change_handler(change_type: str, *args):
    color = ["ambient", "diffuse", "specular"]
    if change_type in color:
        color_code = choose_color()
        if color_code:
            color_code = [value/255 for value in color_code]
            color_code.append(1.0)

    if change_type == "ambient":
        light.change_light(ambient=color_code)
    if change_type == "diffuse":
        light.change_light(diffuse=color_code)
    if change_type == "specular":
        light.change_light(specular=color_code)
    if change_type == "position":
        position = get_coordinates(*args)
        light.change_light(position=position)


def material_change_handler(change_type: str, *args):
    color = ["ambient", "diffuse", "specular"]
    if change_type in color:
        color_code = choose_color()
        if color_code:
            color_code = [value/255 for value in color_code]
            color_code.append(1.0)

    if change_type == "ambient":
        material.change_material(ambient=color_code)
    if change_type == "diffuse":
        material.change_material(diffuse=color_code)
    if change_type == "specular":
        material.change_material(specular=color_code)
    if change_type == "shininess":
        shininess = get_shininess(*args)
        material.change_material(shininess=shininess)


def render_handler():
    render()


def create_gui():
    global interpolation_mode

    root = tk.Tk()
    root.title("Kontrolki Animacji")

    notebook = ttk.Notebook(root)

    # Ustawienia układu głównego okna
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    control_frame = ttk.Frame(notebook)
    control_frame.grid(row=1, column=0, columnspan=2, pady=20)
    frame_slider, transform_mode = create_control_frame(control_frame, save_keyframe_handler)

    light_frame = ttk.Frame(notebook)
    light_frame.grid(row=1, column=0, columnspan=2, pady=20)
    create_light_frame(light_frame, light_change_handler)

    material_frame = ttk.Frame(notebook)
    material_frame.grid(row=1, column=0, columnspan=2, pady=20)
    create_material_frame(material_frame, material_change_handler)

    render_frame = ttk.Frame(notebook)
    render_frame.grid(row=1, column=0, columnspan=2, pady=20)
    create_render_frame(render_frame, render_handler)

    notebook.add(control_frame, text='Klatki')
    notebook.add(light_frame, text="Światło")
    notebook.add(material_frame, text="Materiał")
    notebook.add(render_frame, text="Render")

    notebook.pack(expand=1, fill='both')

    def start_pygame():
        threading.Thread(target=pygame_thread, args=(
            frame_slider, transform_mode), daemon=True).start()

    root.after(100, start_pygame)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
