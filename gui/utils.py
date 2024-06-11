import copy
import tkinter as tk
from tkinter import colorchooser, messagebox

from src.keyframe import Keyframe


def choose_color():
    color_code = colorchooser.askcolor(title="Wybierz kolor")
    return color_code[0]


def get_coordinates(entry_x, entry_y, entry_z):
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        return [x, y, z, 1.0]
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź prawidłowe liczby.")


def get_shininess(value):
    try:
        shininess = float(value.get())
        if shininess not in range(0, 129):
            raise ValueError
        return shininess
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź prawidłową liczbę z zakresu [0, 128].")


def save_keyframe(frame_slider, keyframe_listbox, interpolation_mode,
                  keyframes, translate, rotate, scale):
    current_frame = frame_slider.get()
    keyframe = Keyframe(current_frame, interpolation_mode.get(), list(translate),
                        list(rotate), list(scale))
    keyframes.append(keyframe)
    # Sortuj klatki kluczowe po numerze klatki
    keyframes.sort(key=lambda kf: kf.frame_idx)
    keyframe_listbox.delete(0, tk.END)  # Wyczyść listę
    for kf in keyframes:
        keyframe_listbox.insert(tk.END, f"Klatka {kf.frame_idx}")


def show_keyframe_options(keyframe_frame, keyframe_mode, interpolation_mode):
    keyframe_frame.grid(row=3, column=0, columnspan=2, pady=10)
    keyframe_mode.set("Translation")
    interpolation_mode.set("Constant")


def hide_keyframe_options(keyframe_frame):
    keyframe_frame.grid_forget()
