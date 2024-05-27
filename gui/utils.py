from tkinter import colorchooser, messagebox


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
