import os
import random as rad
import tkinter as tk
from tkinter import messagebox, ttk
import urllib.parse
import webbrowser
import pandas as pd  # type: ignore

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "movies_13plus_and_anime.xlsx")

if not os.path.exists(file_path):
    file_path = r"C:\Users\USER\OneDrive\Desktop\courses\projects\FilmSense\movies_13plus_and_anime.xlsx"

data_base = pd.read_excel(file_path)

if "Watched" not in data_base.columns:
    data_base["Watched"] = False
    data_base.to_excel(file_path, index=False)

current_movie_index = None


def get_movie_title(movie_row):
    """التحقق التلقائي من اسم العمود الذي يحتوي على عنوان الفيلم"""
    possible_columns = [
        "Name",
        "Title",
        "Movie",
        "Film",
        "Movie Title",
        "اسم الفيلم",
        "الاسم",
    ]
    for col in possible_columns:
        if col in movie_row.index and pd.notna(movie_row[col]):
            return str(movie_row[col])

    first_col = movie_row.index[0]
    return str(movie_row[first_col])


def get_random_movie_index():
    return rad.randint(0, len(data_base) - 1)


def update_movie():
    global current_movie_index
    current_movie_index = get_random_movie_index()
    movie = data_base.iloc[current_movie_index]

    title = get_movie_title(movie)
    title_var.set(title)

    details = []
    for col in data_base.columns:
        if col not in ["Watched"] and str(movie[col]) != title:
            details.append(f"• {col}: {movie[col]}")

    details_var.set("\n".join(details))

    is_watched = bool(movie.get("Watched", False))
    update_toggle_button_ui(is_watched)


def toggle_watched_status():
    global current_movie_index
    if current_movie_index is None:
        return

    current_status = bool(data_base.at[current_movie_index, "Watched"])
    new_status = not current_status

    data_base.at[current_movie_index, "Watched"] = new_status
    data_base.to_excel(file_path, index=False)

    update_toggle_button_ui(new_status)


def update_toggle_button_ui(is_watched):
    if is_watched:
        toggle_btn.config(
            text="🟢 Watched (ON)",
            bg="#10b981",
            activebackground="#059669",
            fg="#ffffff",
        )
        status_tag.config(
            text="STATUS: WATCHED", fg="#10b981", bg="#0f172a"
        )
    else:
        toggle_btn.config(
            text="⚪ Not Watched (OFF)",
            bg="#334155",
            activebackground="#475569",
            fg="#94a3b8",
        )
        status_tag.config(
            text="STATUS: UNWATCHED", fg="#94a3b8", bg="#0f172a"
        )


def open_trailer():
    movie_name = title_var.get().strip()
    if movie_name and movie_name != "Unknown Title":
        query = urllib.parse.quote(f"{movie_name} trailer")
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
    else:
        messagebox.showwarning("Warning", "No valid movie title selected.")


root = tk.Tk()
root.title("FilmSense — Modern Movie Discovery")
root.geometry("580x680")
root.configure(bg="#0f172a")
root.resizable(False, False)

header_frame = tk.Frame(root, bg="#0f172a")
header_frame.pack(fill="x", padx=30, pady=(25, 10))

app_title = tk.Label(
    header_frame,
    text="🎬 FilmSense",
    font=("Segoe UI", 24, "bold"),
    fg="#f8fafc",
    bg="#0f172a",
)
app_title.pack(anchor="w")

app_subtitle = tk.Label(
    header_frame,
    text="Discover your next favorite movie instantly",
    font=("Segoe UI", 10),
    fg="#64748b",
    bg="#0f172a",
)
app_subtitle.pack(anchor="w", pady=(2, 0))

card = tk.Frame(
    root, bg="#1e293b", highlightbackground="#334155", highlightthickness=1
)
card.pack(fill="both", expand=True, padx=30, pady=15)

status_tag = tk.Label(
    card,
    text="STATUS: UNWATCHED",
    font=("Segoe UI", 8, "bold"),
    fg="#94a3b8",
    bg="#0f172a",
    padx=8,
    pady=3,
)
status_tag.pack(anchor="ne", padx=20, pady=(15, 0))

title_var = tk.StringVar()
movie_title_label = tk.Label(
    card,
    textvariable=title_var,
    font=("Segoe UI", 16, "bold"),
    fg="#f1f5f9",
    bg="#1e293b",
    wraplength=480,
    justify="left",
)
movie_title_label.pack(anchor="w", padx=20, pady=(5, 10))

separator = tk.Frame(card, bg="#334155", height=1)
separator.pack(fill="x", padx=20, pady=5)

details_var = tk.StringVar()
details_label = tk.Label(
    card,
    textvariable=details_var,
    font=("Segoe UI", 10),
    fg="#cbd5e1",
    bg="#1e293b",
    justify="left",
    anchor="nw",
    wraplength=480,
)
details_label.pack(fill="both", expand=True, padx=20, pady=15)

controls_frame = tk.Frame(card, bg="#1e293b")
controls_frame.pack(fill="x", padx=20, pady=(0, 20))

toggle_btn = tk.Button(
    controls_frame,
    text="⚪ Not Watched (OFF)",
    font=("Segoe UI", 10, "bold"),
    bg="#334155",
    fg="#94a3b8",
    activebackground="#475569",
    activeforeground="#ffffff",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=8,
    command=toggle_watched_status,
)
toggle_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

trailer_btn = tk.Button(
    controls_frame,
    text="▶ Watch Trailer",
    font=("Segoe UI", 10, "bold"),
    bg="#dc2626",
    fg="#ffffff",
    activebackground="#b91c1c",
    activeforeground="#ffffff",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=8,
    command=open_trailer,
)
trailer_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

retry_button = tk.Button(
    root,
    text="🎲 Recommend Another Movie",
    font=("Segoe UI", 12, "bold"),
    bg="#6366f1",
    fg="#ffffff",
    activebackground="#4f46e5",
    activeforeground="#ffffff",
    bd=0,
    cursor="hand2",
    pady=12,
    command=update_movie,
)
retry_button.pack(fill="x", padx=30, pady=(5, 25))

update_movie()

root.mainloop()
