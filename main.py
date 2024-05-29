import copy
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
from gui.utils import get_coordinates, get_shininess, choose_color, save_keyframe
from src.camera import Camera
from src.interpolation import interpolate
from src.keyframe import Keyframe
from src.load_file import load_obj
from src.light import Light, Material
import sys
import math
import signal
import tkinter as tk
from tkinter import ttk
import threading
from src.render import save_frame, save_video

keyframes = []
interpolation_mode = None
translate = [0, 0, 0]
rotate = [0, 0, 0]
scale = [1, 1, 1]

rendering = False

all_frames = {}

def draw_grid(zoom, fov, aspect):
    """Draws a simple grid on the XY plane, adaptive to the view range."""
    glDisable(GL_LIGHTING)  # Disable lighting to ensure the grid color is not affected

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


def update_transformations(frame_slider):
    global keyframes, translate, rotate, scale

    if not keyframes:
        return translate, rotate, scale

    current_frame = frame_slider.get()
    prev_keyframe = None
    next_keyframe = None

    for i, keyframe in enumerate(keyframes):
        frame = keyframe.frame_idx
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

    start_frame = prev_keyframe.frame_idx
    start_translate = prev_keyframe.translation
    start_rotate = prev_keyframe.rotation
    start_scale = prev_keyframe.scale

    end_frame = next_keyframe.frame_idx
    end_translate = next_keyframe.translation
    end_rotate = next_keyframe.rotation
    end_scale = next_keyframe.scale

    interpolation_mode = next_keyframe.interpolation_mode

    if start_frame == end_frame:
        return start_translate, start_rotate, start_scale

    alpha = (current_frame - start_frame) / (end_frame - start_frame)
    translate = [interpolate(start_translate[i], end_translate[i],
                             alpha, interpolation_mode) for i in range(3)]
    rotate = [interpolate(start_rotate[i], end_rotate[i],
                          alpha, interpolation_mode) for i in range(3)]
    scale = [interpolate(start_scale[i], end_scale[i], alpha,
                         interpolation_mode) for i in range(3)]

    return translate, rotate, scale


def pygame_thread(frame_slider, transform_mode, interpolation_mode):
    global keyframes, translate, rotate, scale, material, light, all_frames, rendering

    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Set up the signal handler for graceful exit
    # signal.signal(signal.SIGINT, handle_exit)
    if file_path:
        model = load_obj(file_path)

    # Set up
    material = Material()
    light = Light(material)
    camera = Camera()

    near_render_distance = 0.1
    far_render_distance = 1000

    grid = True
    running = True

    while running:
        if rendering:
            print("pygame: rendering set true")
        keyframe = Keyframe(frame_slider.get(), interpolation_mode.get(), translate, rotate, scale)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    grid = not grid
                else:
                    camera.change_camera_position(event)
                # Translacja
                if transform_mode.get() == "Translation":
                    keyframe.change_translation(event)
                # Rotacja
                elif transform_mode.get() == "Rotation":
                    keyframe.change_rotation(event)
                # Skalowanie
                elif transform_mode.get() == "Scaling":
                    keyframe.change_scale(event)

        translate, rotate, scale = keyframe.translation, keyframe.rotation, keyframe.scale
        # Ensure elevation is within -90 to 90 degrees to avoid gimbal lock
        camera.elevation = max(-90, min(90, camera.elevation))

        # Convert spherical coordinates to Cartesian coordinates for the camera
        eye_x = camera.calculate_eye_x()
        eye_y = camera.calculate_eye_y()
        eye_z = camera.calculate_eye_z()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set the perspective projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(camera.fov, (display[0] / display[1]),
                       near_render_distance, far_render_distance)

        light.setup_lighting()

        # Set the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye_x, eye_y, eye_z,  # Eye position (camera)
                  0, 0, 0,             # Look at origin
                  0, 0, 1)             # Up vector (z-axis)

        # Draw the grid
        if grid and not rendering:
            draw_grid(camera.zoom, camera.fov, display[0] / display[1])

        # Apply transformations and draw the model
        glPushMatrix()
        if keyframes:
            keyframe.translation, keyframe.rotation, keyframe.scale = update_transformations(frame_slider)

        glTranslatef(*translate)
        glRotatef(rotate[0], 1, 0, 0)
        glRotatef(rotate[1], 0, 1, 0)
        glRotatef(rotate[2], 0, 0, 1)
        glScalef(*scale)

        model.draw_model()
        glPopMatrix()

        # Capture and save the current frame
        if rendering:
            print(f"pygame: capturing frame {frame_slider.get()}")
            frame_idx = frame_slider.get()
            print(frame_idx)
            frame = save_frame()
            all_frames[frame_idx] = frame
            if frame_slider.get() < 100:
                frame_slider.set(frame_idx + 1)
            else:
                rendering = False
                save_video(dict(sorted(all_frames.items())).values())

        # Update display
        pygame.display.flip()
        pygame.time.wait(10)

    for kf in keyframes:
        print(kf)


def save_keyframe_handler(frame_slider, keyframe_listbox, interpolation_mode):
    save_keyframe(frame_slider, keyframe_listbox, interpolation_mode,
                  keyframes, translate, rotate, scale)
    for keyframe in keyframes:
        print(keyframe)


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


def render_handler(frame_slider):
    global rendering
    rendering = True
    frame_slider.set(0)


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
    frame_slider, transform_mode, interpolation_mode = create_control_frame(
        control_frame, save_keyframe_handler, render_handler)

    light_frame = ttk.Frame(notebook)
    light_frame.grid(row=1, column=0, columnspan=2, pady=20)
    create_light_frame(light_frame, light_change_handler)

    material_frame = ttk.Frame(notebook)
    material_frame.grid(row=1, column=0, columnspan=2, pady=20)
    create_material_frame(material_frame, material_change_handler)

    notebook.add(control_frame, text='Klatki')
    notebook.add(light_frame, text="Światło")
    notebook.add(material_frame, text="Materiał")

    notebook.pack(expand=1, fill='both')

    def start_pygame():
        threading.Thread(target=pygame_thread, args=(
            frame_slider, transform_mode, interpolation_mode), daemon=True).start()

    root.after(100, start_pygame)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
