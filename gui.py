import tkinter as tk
from tkinter import colorchooser


def choose_color():
    color_code = colorchooser.askcolor(title="Wybierz kolor")
    return color_code[0]


def create_light_frame(frame, color_change_handler):
    ambient_label = tk.Label(frame, text="Ambient")
    ambient_label.grid(row=2, column=0, pady=5)
    choose_ambient_color_button = tk.Button(frame, text="Wybierz kolor ambient", command=lambda: color_change_handler("ambient"))
    choose_ambient_color_button.grid(row=3, column=0, pady=5)

    diffuse_label = tk.Label(frame, text="Diffuse")
    diffuse_label.grid(row=4, column=0, pady=5)
    choose_diffuse_color_button = tk.Button(frame, text="Wybierz kolor diffuse", command=lambda: color_change_handler("diffuse"))
    choose_diffuse_color_button.grid(row=5, column=0, pady=5)

    specular_label = tk.Label(frame, text="Specular")
    specular_label.grid(row=6, column=0, pady=5)
    choose_specular_color_button = tk.Button(frame, text="Wybierz kolor specular", command=lambda: color_change_handler("specular"))
    choose_specular_color_button.grid(row=7, column=0, pady=5)