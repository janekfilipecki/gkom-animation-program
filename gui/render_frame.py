import tkinter as tk


def create_render_frame(frame, render_handler):
    render_button = tk.Button(frame, text="Renderuj animację", command=render_handler)
    render_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
