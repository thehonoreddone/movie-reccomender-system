import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
import pandas as pd
import pickle

def fetch_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None

def recommend_movies():
    selected_movie = movie_combobox.get()
    if not selected_movie:
        messagebox.showerror("Error", "Please select a movie")
        return
    try:
        index = movies[movies['title'] == selected_movie].index[0]
        distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
        recommended_names = []
        recommended_posters = []
        for i in distances[1:6]:
            id = movies.iloc[i[0]].id
            recommended_names.append(movies.iloc[i[0]].title)
            poster_url = fetch_poster(id)
            recommended_posters.append(poster_url if poster_url else "")

        update_ui(recommended_names, recommended_posters)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_ui(movie_names, poster_urls):
    for i in range(5):
        movie_labels[i].config(text=movie_names[i])
        if poster_urls[i]:
            response = requests.get(poster_urls[i])
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize((100, 150), Image.LANCZOS)
            img = ImageTk.PhotoImage(img_data)
            poster_labels[i].config(image=img)
            poster_labels[i].image = img

def populate_movies():
    movie_combobox['values'] = movies['title'].tolist()

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

root = tk.Tk()
root.title("Film Recommender System")
root.geometry("800x600")

tk.Label(root, text="Choose a film:").pack(pady=10)
movie_combobox = ttk.Combobox(root, width=50)
movie_combobox.pack(pady=5)

populate_movies()

tk.Button(root, text="Recommend", command=recommend_movies).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

movie_labels = [tk.Label(frame, text="", wraplength=150) for _ in range(5)]
poster_labels = [tk.Label(frame) for _ in range(5)]

for i in range(5):
    poster_labels[i].grid(row=0, column=i, padx=5)
    movie_labels[i].grid(row=1, column=i, padx=5)

root.mainloop()
