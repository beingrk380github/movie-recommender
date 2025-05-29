# app.py

import streamlit as st
import pandas as pd
import pickle
import requests

# Load data and model
import os

MOVIE_LIST_PATH = "model/movie_list.pkl"
SIMILARITY_PATH = "model/similarity.pkl"

if not os.path.exists(MOVIE_LIST_PATH) or not os.path.exists(SIMILARITY_PATH):
    st.error(
        f"Required model files not found.\n\n"
        f"Please ensure '{MOVIE_LIST_PATH}' and '{SIMILARITY_PATH}' exist.\n\n"
        f"You may need to train your model and save these files in the 'model' directory."
    )
    st.markdown(
        """
        **To generate the required files, run your training script or notebook that creates `movie_list.pkl` and `similarity.pkl` in the `model` folder.**
        """
    )
    st.stop()

movies = pickle.load(open(MOVIE_LIST_PATH, "rb"))
similarity = pickle.load(open(SIMILARITY_PATH, "rb"))

# TMDB API Setup (replace with your TMDB API key if needed)
TMDB_API_KEY = "YOUR_TMDB_API_KEY"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie_title):
    index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_titles = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_titles, recommended_posters

# UI Design
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #000;
        color: #fff;
    }
    h1, h2, h3, h4, h5 {
        color: #ff4d4d;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

if st.button("Recommend 🎥"):
    names, posters = recommend(selected_movie)
    
    st.subheader(f"Because you liked *{selected_movie}*, you might also enjoy:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], caption=names[i], use_column_width=True)

# Footer
st.markdown("""
    <hr style="border: 1px solid #444;">
    <div style="text-align: center;">
        Built by <a href="https://www.linkedin.com/in/rambabukumargiri/" target="_blank" style="color: #ff4d4d;">Rambabu Kumar</a> | 2025
    </div>
""", unsafe_allow_html=True)
