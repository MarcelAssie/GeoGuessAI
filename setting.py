import streamlit as st

def display_settings(game):
    st.title("⚙️ Paramètres de l'interface")
    game.max_rounds = st.slider("Nombre de manches", 1, 10, game.max_rounds)