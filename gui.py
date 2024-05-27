import tkinter as tk
from tkinter import colorchooser, messagebox


def choose_color():
    color_code = colorchooser.askcolor(title="Wybierz kolor")
    return color_code[0]


def get_coordinates(entry_x, entry_y, entry_z):
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        messagebox.showinfo("Współrzędne", f"x: {x}, y: {y}, z: {z}")
        return [x, y, z, 1.0]
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź prawidłowe liczby.")


def create_light_frame(frame, light_change_handler):
    position_label = tk.Label(frame, text="Kolor")
    position_label.grid(row=2, column=0, padx=10, pady=5)

    choose_ambient_color_button = tk.Button(frame, text="Wybierz kolor ambient", command=lambda: light_change_handler("ambient"))
    choose_ambient_color_button.grid(row=2, column=1, columnspan=3, padx=10, pady=5)

    choose_diffuse_color_button = tk.Button(frame, text="Wybierz kolor diffuse", command=lambda: light_change_handler("diffuse"))
    choose_diffuse_color_button.grid(row=4, column=1, columnspan=3, padx=10, pady=5)

    choose_specular_color_button = tk.Button(frame, text="Wybierz kolor specular", command=lambda: light_change_handler("specular"))
    choose_specular_color_button.grid(row=6, column=1, columnspan=3, padx=10, pady=5)

    position_label = tk.Label(frame, text="Pozycja")
    position_label.grid(row=8, column=0, padx=10, pady=5)

    label_x = tk.Label(frame, text="x:")
    label_x.grid(row=8, column=1, pady=10)

    entry_x = tk.Entry(frame, width=5)
    entry_x.grid(row=8, column=2, pady=10)

    label_y = tk.Label(frame, text="y:")
    label_y.grid(row=9, column=1, pady=10)

    entry_y = tk.Entry(frame, width=5)
    entry_y.grid(row=9, column=2, pady=10)

    label_z = tk.Label(frame, text="z:")
    label_z.grid(row=10, column=1, pady=10)

    entry_z = tk.Entry(frame, width=5)
    entry_z.grid(row=10, column=2, pady=10)

    submit_button = tk.Button(frame, text="Zatwierdź pozycję", command=lambda: light_change_handler("position", entry_x, entry_y, entry_z))
    submit_button.grid(row=11, column=1, columnspan=2, padx=10, pady=10)