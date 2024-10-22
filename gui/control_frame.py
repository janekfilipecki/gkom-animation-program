import tkinter as tk
from gui.utils import hide_keyframe_options, show_keyframe_options


def create_control_frame(frame, save_keyframe_handler, render_handler):
    frame_slider = tk.Scale(frame, from_=0,
                            to=100, orient=tk.HORIZONTAL, label="Klatki")
    frame_slider.grid(row=1, column=0, pady=5)

    # Pole do wprowadzania ilości klatek
    frame_count_entry = tk.Entry(frame)
    frame_count_entry.grid(row=2, column=0, pady=5)

    # Przycisk do aktualizacji wartości maksymalnej slidera
    update_button = tk.Button(frame, text="Ustaw ilość klatek", command=lambda: update_slider_max(frame_slider, frame_count_entry))
    update_button.grid(row=3, column=0, pady=5)


    keyframe_label = tk.Label(frame, text="Keyframes: []")
    keyframe_label.grid(row=4, column=0, pady=5)

    keyframe_listbox = tk.Listbox(frame, height=5)
    keyframe_listbox.grid(row=5, column=0, pady=5)

    keyframe_mode = tk.StringVar()
    interpolation_mode = tk.StringVar()
    transform_mode = tk.StringVar(value="Translation")

    keyframe_frame = tk.Frame(frame)
    tk.Label(keyframe_frame, text="Wybierz tryb przekształcenia:").grid(
        row=0, column=0, pady=5)
    tk.Radiobutton(keyframe_frame, text="Translacja", variable=transform_mode,
                   value="Translation").grid(row=1, column=0, sticky=tk.W, pady=2)
    tk.Radiobutton(keyframe_frame, text="Rotacja", variable=transform_mode,
                   value="Rotation").grid(row=2, column=0, sticky=tk.W, pady=2)
    tk.Radiobutton(keyframe_frame, text="Skalowanie", variable=transform_mode,
                   value="Scaling").grid(row=3, column=0, sticky=tk.W, pady=2)

    tk.Label(keyframe_frame, text="Wybierz interpolację:").grid(
        row=4, column=0, pady=5)
    tk.Radiobutton(keyframe_frame, text="Stała", variable=interpolation_mode,
                   value="Constant").grid(row=5, column=0, sticky=tk.W, pady=2)
    tk.Radiobutton(keyframe_frame, text="Liniowa", variable=interpolation_mode,
                   value="Linear").grid(row=6, column=0, sticky=tk.W, pady=2)

    tk.Button(keyframe_frame, text="Save", command=lambda: [save_keyframe_handler(frame_slider, keyframe_listbox, interpolation_mode), hide_keyframe_options(
        keyframe_frame)]).grid(row=7, column=0, sticky=tk.W, padx=5, pady=10)
    tk.Button(keyframe_frame, text="Odrzuć", command=lambda: hide_keyframe_options(
        keyframe_frame)).grid(row=7, column=1, sticky=tk.E, padx=5, pady=10)

    tk.Button(frame, text="Wstaw Klatkę Kluczową", command=lambda: show_keyframe_options(
        keyframe_frame, keyframe_mode, interpolation_mode)).grid(row=6, column=0, pady=10)

    render_button = tk.Button(frame, text="Renderuj animację", command=lambda: render_handler(frame_slider))
    render_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    return frame_slider, transform_mode, interpolation_mode, frame_count_entry, update_button


    # Funkcja aktualizująca maksymalną wartość slidera
def update_slider_max(frame_slider, frame_count_entry):
    try:
        max_value = int(frame_count_entry.get())
        frame_slider.config(to=max_value)
        frame_count_entry.delete(0, tk.END)
        frame_count_entry.insert(0, "")
    except ValueError:
        frame_count_entry.delete(0, tk.END)
        frame_count_entry.insert(0, 'Invalid input')
