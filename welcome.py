import streamlit as st
import time


def stream_text():
    """Générateur pour l'effet de texte animé avec conservation du markdown"""
    sections = [
        "**🧠 Concept:**",
        "Affrontez une IA sur son terrain : la connaissance de l'espace !",
        "Deux modes au choix :",
        "- **Mode 1: Adresse → Coordonnées**",
        "- **Mode 2: Coordonnées → Adresse**",
        "",
        "**🎯 Objectif:**",
        "Soyez plus précis que l'IA pour gagner des points !",
        "",
        "**🏆 Scoring:**",
        "- Mode 1: Points selon la distance (plus c'est précis, plus c'est payant)",
        "- Mode 2: Points selon la précision de l'adresse (communes, nom de la voie, numéro de la voie)"
    ]

    for section in sections:
        if section.startswith(("**", "-")):  # Si c'est du markdown important
            st.markdown(section)
            time.sleep(0.3)
        else:
            for word in section.split():
                yield word + " "
                time.sleep(0.02)
            yield "\n\n"  # Saut de ligne


def display_welcome(game_instance):
    """Affiche l'interface de bienvenue et récupère les infos du joueur"""
    # Configuration de la page
    st.set_page_config(layout="wide")

    # Section titre + image
    col_title, col_img = st.columns([2, 1])
    with col_title:
        st.title("🌍 GeoGuessAI - Duel Géospatial")
    with col_img:
        st.image("../Images/welcome_image.png", width=300)

    # Section Comment jouer avec bouton aligné
    st.markdown("---")

    with st.expander("📌 Comment jouer ?", expanded=True):
        placeholder = st.empty()
        full_text = ""

        for chunk in stream_text():
            if isinstance(chunk, str):
                full_text += chunk
                placeholder.markdown(full_text)

        st.write("\n")
        if st.button("Plus de détails", key="more_details"):
            game_instance.current_page = "About"
            st.rerun()

    # Formulaire joueur
    st.markdown("---")
    st.subheader("👤 Informations joueur")
    col1, col2 = st.columns(2)
    with col1:
        game_instance.player_name = st.text_input("Votre prénom/pseudo:", "Joueur")
    with col2:
        game_instance.player_gender = st.selectbox(
            "Genre:",
            ["Non renseigné", "Masculin", "Féminin"]
        )

    # Sélection mode de jeu
    st.markdown("---")
    st.subheader("🎮 Choisissez votre mode de jeu:")
    game_instance.game_mode = st.radio(
        "Mode de jeu:",
        options=("Adresse → Coordonnées", "Coordonnées → Adresse"),
        horizontal=True,
        index=0
    )

    # Bouton de démarrage
    st.markdown("---")
    if st.button(
            "Commencer le jeu 🚀",
            type="primary",
            use_container_width=True,
            help="Cliquez pour lancer une nouvelle partie"
    ):
        game_instance.current_round = 1
        game_instance.start_round()
        st.rerun()

    # Pied de page
    st.markdown("---")
    st.caption("Marcel Assie - GeoAI Engineer © 2025 GeoGuessAI - Tous droits réservés")