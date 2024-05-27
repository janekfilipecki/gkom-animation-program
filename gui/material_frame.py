import tkinter as tk


def create_material_frame(frame, material_change_handler):
    position_label = tk.Label(frame, text="Kolor")
    position_label.grid(row=2, column=0, padx=10, pady=5)

    choose_ambient_color_button = tk.Button(frame, text="Wybierz kolor ambient", command=lambda: material_change_handler("ambient"))
    choose_ambient_color_button.grid(row=2, column=1, columnspan=3, padx=10, pady=5)

    choose_diffuse_color_button = tk.Button(frame, text="Wybierz kolor diffuse", command=lambda: material_change_handler("diffuse"))
    choose_diffuse_color_button.grid(row=4, column=1, columnspan=3, padx=10, pady=5)

    choose_specular_color_button = tk.Button(frame, text="Wybierz kolor specular", command=lambda: material_change_handler("specular"))
    choose_specular_color_button.grid(row=6, column=1, columnspan=3, padx=10, pady=5)

    label_shininess = tk.Label(frame, text="Połyskliwość")
    label_shininess.grid(row=8, column=0, pady=10)

    entry_shininess = tk.Entry(frame, width=5)
    entry_shininess.grid(row=8, column=2, pady=10)

    submit_button = tk.Button(frame, text="Zatwierdź", command=lambda: material_change_handler("shininess", entry_shininess))
    submit_button.grid(row=8, column=3, columnspan=2, padx=10, pady=10)
