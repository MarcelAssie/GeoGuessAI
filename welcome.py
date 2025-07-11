import streamlit as st

def display_welcome(game):
    """Affiche l'interface de bienvenue et récupère les infos du joueur"""
    st.title("🌍 GeoGuessAI - Duel Géospatial")

    with st.expander("📌 Comment jouer ?", expanded=True):
        st.markdown("""
        **🧠 Concept:**  
        Affrontez une IA sur son terrain : la connaissance de l'espace !  
        Deux modes au choix :  
        - **Mode 1: Adresse → Coordonnées**  
        - **Mode 2: Coordonnées → Adresse**  

        **🎯 Objectif:**  
        Soyez plus précis que l'IA pour gagner des points !  

        **🏆 Scoring:**  
        - Mode 1: Points selon la distance (plus c'est précis, plus c'est payant)  
        - Mode 2: Points pour la commune (+1), voie (+2), numéro exact (+3)  
        """)

    col1, col2 = st.columns(2)
    with col1:
        game.player_name = st.text_input("Votre prénom/pseudo:", "Joueur")
    with col2:
        game.player_gender = st.selectbox("Genre:", ["Non renseigné", "Masculin", "Féminin"])

    st.markdown("---")
    st.subheader("Choisissez votre mode de jeu:")
    game.game_mode = st.radio(
        "Mode de jeu:",
        options=("Adresse → Coordonnées", "Coordonnées → Adresse"),
        horizontal=True
    )

    if st.button("Commencer le jeu 🚀", type="primary"):
        game.current_round = 1
        game.start_round()
        st.rerun()