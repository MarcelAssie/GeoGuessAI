from app import GeospatialGame
import streamlit as st


def main():
    # Initialisation du jeu avec gestion d'état améliorée
    if 'game' not in st.session_state:
        st.session_state.game = GeospatialGame()

    # Lancement du jeu
    st.session_state.game.run()


if __name__ == "__main__":
    main()