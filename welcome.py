import streamlit as st
import time, base64

def get_image_as_base64(file):
    """Lit un fichier image et le retourne en chaîne Base64."""
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def stream_text():
    """Générateur pour l'effet de texte animé avec conservation du markdown"""
    sections = [
        "**Concept:**",
        "Affrontez une IA sur son terrain : la connaissance de l'espace !",
        "Deux modes au choix :",
        "- **Mode 1: Adresse → Coordonnées**",
        "- **Mode 2: Coordonnées → Adresse**",
        "",
        "**Objectif:** Soyez plus précis que l'IA pour gagner des points !",
        "",
        "**Scoring:**",
        "- Mode 1: Points selon la distance (plus c'est précis, plus c'est payant)",
        "- Mode 2: Points selon la précision de l'adresse (communes, nom de la voie, numéro de la voie)"
    ]
    for section in sections:
        if section.startswith(("**", "-")):  # Si c'est du markdown important
            st.markdown(section)
            time.sleep(0.02)
        else:
            for word in section.split():
                yield word + " "
                time.sleep(0.02)
            yield "\n\n"  # Saut de ligne


@st.dialog("Configuration")
def show_game_config_modal(game_instance):
    """Fenêtre modale pour la configuration du jeu"""
    st.subheader("Informations joueur")

    # Formulaire joueur
    col1, col2 = st.columns(2)
    with col1:
        player_name = st.text_input("Votre pseudo:", value=game_instance.player_name or "Joueur")
    with col2:
        player_gender = st.selectbox(
            "Genre:",
            ["Non renseigné", "Masculin", "Féminin"],
            index=["Non renseigné", "Masculin", "Féminin"].index(game_instance.player_gender or "Non renseigné")
        )

    st.markdown("---")
    st.subheader("Mode de jeu et manches")

    # Sélection mode de jeu
    game_mode = st.radio(
        "Choisissez votre mode ",
        options=("Adresse → Coordonnées", "Coordonnées → Adresse"),
        horizontal=True,
        index=0 if not game_instance.game_mode else
        (0 if game_instance.game_mode == "Adresse → Coordonnées" else 1)
    )
    game_instance.max_rounds = st.slider(
        "Choisissez le nombre de manches",
        1, 20, game_instance.max_rounds,
        help="Détermine le nombre total de tours dans une partie"
    )

    # Boutons d'action
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Annuler", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("Commencer le jeu", type="primary", use_container_width=True):
            # Sauvegarder les paramètres
            game_instance.player_name = player_name
            game_instance.player_gender = player_gender
            game_instance.game_mode = game_mode
            game_instance.current_round = 1
            game_instance.start_round()
            st.rerun()


def display_welcome(game_instance):
    """Affiche l'interface de bienvenue avec le titre sur l'image de bannière."""
    # Configuration de la page
    st.set_page_config(layout="wide")

    col0, col1 = st.columns([2,1])

    with col0 :
        img_file = "../Images/welcome_image.png"
        # Conversion de l'image en Base64
        img_base64 = get_image_as_base64(img_file)

        # Injection de CSS et HTML avec l'image en Base64
        st.markdown(
            f"""
                <style>
                .banner {{
                    position: relative;
                    width: 100%;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .banner img {{
                    width: 100%;
                    height: auto;
                    object-fit: cover;
                    border-radius: 1%;
                }}
                .banner h1 {{
                    position: absolute;
                    bottom: 0;
                    left: 50%;
                    transform: translateX(-50%);
                    color: white;
                    font-size: 3rem;
                    text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
                    margin: 0;
                    background-color: rgba(0, 0, 0, 0.8);
                    padding: 20px 40px;
                    border-radius: 10px 10px 0 0;
                    font-weight: bold;
                    width: 100%;
                }}
                </style>

                <div class="banner">
                    <img src="data:image/png;base64,{img_base64}" alt="Bannière GeoGuessAI">
                    <h1>🌍 GeoGuessAI - Duel Géospatial</h1>
                </div>
                """,
            unsafe_allow_html=True,
        )
        col2, col3, col34 = st.columns([1, 2, 1])
        with col3:
            if st.button(
                    "Jouer",
                    type="primary",
                    use_container_width=True,
                    help="Cliquez pour configurer vos paramètres et lancer le jeu"
            ):
                show_game_config_modal(game_instance)


    with col1:
        # Section Comment jouer
        with st.expander("Comment jouer ?", expanded=True):
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


