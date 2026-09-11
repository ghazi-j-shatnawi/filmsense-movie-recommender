import random as rad
import tkinter as tk
from tkinter import ttk
import pandas as pd  # type: ignore

file_path = r"C:\Users\USER\OneDrive\Desktop\courses\projects\FilmSense\movies_13plus_and_anime.xlsx"
data_base = pd.read_excel(file_path)


def get_random_movie_info():
    random_index = rad.randint(0, len(data_base) - 1)
    selected_movie = data_base.iloc[random_index]

    info_text = ""
    for column, value in selected_movie.items():
        info_text += f"{column}: {value}\n"

    return info_text


def update_movie():
    movie_info = get_random_movie_info()
    info_label.config(text=movie_info)


root = tk.Tk()
root.title("FilmSense - Movie Recommendation")
root.geometry("500x450")
root.configure(bg="#1f1f2e")

title_label = tk.Label(
    root,
    text="🎬 Tonight's Featured Movie",
    font=("Helvetica", 16, "bold"),
    fg="#ffffff",
    bg="#1f1f2e",
)
title_label.pack(pady=15)

frame = tk.Frame(root, bg="#2d2d44", padx=15, pady=15)
frame.pack(fill="both", expand=True, padx=20, pady=10)

info_label = tk.Label(
    frame,
    text="",
    font=("Helvetica", 11),
    fg="#e0e0e0",
    bg="#2d2d44",
    justify="left",
    anchor="w",
    wraplength=420,
)
info_label.pack(fill="both", expand=True)

retry_button = tk.Button(
    root,
    text="🔄 Pick Another Movie",
    font=("Helvetica", 12, "bold"),
    bg="#e50914",
    fg="white",
    activebackground="#b20710",
    activeforeground="white",
    bd=0,
    padx=15,
    pady=8,
    command=update_movie,
)
retry_button.pack(pady=15)

update_movie()

root.mainloop()
