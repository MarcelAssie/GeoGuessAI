import streamlit as st


def display_settings(game):
    """Affiche les paramètres de jeu avec une interface utilisateur complète"""
    st.title("⚙️ Paramètres du jeu")

    with st.container(border=True):
        st.subheader("🎮 Configuration de la partie")
        col1, col2 = st.columns(2)

        with col1:
            # Paramètre principal du nombre de manches
            game.max_rounds = st.slider(
                "Nombre de manches",
                1, 20, game.max_rounds,
                help="Détermine le nombre total de tours dans une partie"
            )

            # Difficulté du jeu
            difficulty_options = {
                "Facile": {"tolerance": 200, "ai_delay": 2},
                "Normal": {"tolerance": 100, "ai_delay": 1},
                "Difficile": {"tolerance": 50, "ai_delay": 0.5},
                "Expert": {"tolerance": 20, "ai_delay": 0.2}
            }
            selected_difficulty = st.selectbox(
                "Niveau de difficulté",
                list(difficulty_options.keys()),
                index=1,
                help="Influence la précision requise et la vitesse de l'IA"
            )
            game.tolerance = difficulty_options[selected_difficulty]["tolerance"]
            game.ai_delay = difficulty_options[selected_difficulty]["ai_delay"]

        with col2:
            # Mode de jeu par défaut
            game.default_mode = st.radio(
                "Mode de jeu par défaut",
                options=("Adresse → Coordonnées", "Coordonnées → Adresse"),
                index=0 if game.game_mode == "Adresse → Coordonnées" else 1,
                horizontal=True
            )

            # Activation des bonus
            game.enable_bonus = st.checkbox(
                "Activer les bonus de précision",
                value=True,
                help="Donne des points supplémentaires pour les réponses très précises"
            )

    with st.container(border=True):
        st.subheader("🎨 Personnalisation de l'interface")

        # Sélection du thème
        theme_col, accent_col = st.columns(2)

        with theme_col:
            # Sélection du thème
            current_theme = st.selectbox(
                "Thème de l'application",
                ["Auto", "Clair", "Sombre"],
                index=0 if game.theme == "Auto" else 1 if game.theme == "Clair" else 2,
                help="Change l'apparence visuelle de l'application"
            )

            # apply_theme_css(game)
            # Appliquer immédiatement le thème via query parameters
            if current_theme != game.theme:
                game.theme = current_theme
                if current_theme == "Clair":
                    st.query_params.theme = "light"
                elif current_theme == "Sombre":
                    st.query_params.theme = "dark"
                else:
                    st.query_params.theme = "auto"
                st.rerun()

        with accent_col:
            game.accent_color = st.color_picker(
                "Couleur d'accent",
                "#00C0F2",
                help="Couleur principale des boutons et éléments interactifs"
            )

        # Paramètres d'affichage
        game.animation_speed = st.slider(
            "Vitesse des animations",
            0.1, 2.0, 1.0, 0.1,
            help="Contrôle la vitesse des effets visuels"
        )

        game.enable_sound = st.checkbox(
            "Activer les effets sonores",
            value=True
        )

    with st.container(border=True):
        st.subheader("🔧 Paramètres avancés")

        # Options pour les joueurs expérimentés
        game.enable_debug = st.checkbox(
            "Mode debug",
            value=False,
            help="Affiche des informations techniques pour le développement"
        )

        game.allow_retry = st.checkbox(
            "Autoriser les nouvelles tentatives",
            value=True,
            help="Permet de rejouer une manche ratée (avec pénalité)"
        )

        if st.button("Réinitialiser les paramètres par défaut", type="secondary"):
            game.max_rounds = 3
            game.tolerance = 100
            game.theme = "Auto"
            game.enable_bonus = True
            st.rerun()

    # Sauvegarde automatique des paramètres
    if st.button("Sauvegarder les paramètres", type="primary"):
        st.success("Paramètres enregistrés avec succès!")
        st.balloons()


def _apply_theme_css(game):
    pass
    # """Applique un thème clair ou sombre agréable à l'œil avec couleurs harmonieuses"""
    # css = """
    # <style>
    #     :root {{
    #         --primary-color: {accent_color};
    #         --background-color: {bg_color};
    #         --secondary-background-color: {secondary_bg};
    #         --text-color: {text_color};
    #         --font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    #     }}
    #
    #     body, .stApp {{
    #         background-color: var(--background-color) !important;
    #         color: var(--text-color) !important;
    #         font-family: var(--font-family) !important;
    #     }}
    #
    #     h1, h2, h3, h4, h5, h6 {{
    #         color: var(--primary-color) !important;
    #     }}
    #
    #     .stMarkdown, .stText, .stAlert, .stButton>button, .stSelectbox,
    #     .stTextInput, .stNumberInput, .stTextArea, .stSlider {{
    #         color: var(--text-color) !important;
    #         font-family: var(--font-family) !important;
    #     }}
    #
    #     /* Sidebar */
    #     .css-1d391kg, .st-emotion-cache-1cypcdb {{
    #         background-color: var(--secondary-background-color) !important;
    #     }}
    #
    #     /* Widgets champs de texte */
    #     .stTextInput>div>div>input, .stNumberInput>div>div>input,
    #     .stSelectbox>div>select, .stTextArea>div>textarea {{
    #         background-color: var(--secondary-background-color) !important;
    #         color: var(--text-color) !important;
    #         border: 1px solid #666 !important;
    #     }}
    #
    #     /* Boutons */
    #     .stButton>button {{
    #         background-color: var(--primary-color) !important;
    #         color: #fff !important;
    #         border-radius: 8px !important;
    #         padding: 0.5em 1em !important;
    #         font-weight: bold !important;
    #         transition: background-color 0.3s ease;
    #     }}
    #
    #     .stButton>button:hover {{
    #         background-color: #444 !important;
    #         color: #fff !important;
    #     }}
    #
    #     /* Amélioration pour sliders et inputs */
    #     .stSlider>div {{
    #         color: var(--text-color) !important;
    #     }}
    # </style>
    # """.format(
    #     accent_color=game.accent_color or ("#4CAF50" if game.theme == "Clair" else "#00E0A8"),  # Vert ou turquoise
    #     bg_color="#F7F9FC" if game.theme == "Clair" else "#12151C",  # Doux gris bleuté ou gris charbon
    #     secondary_bg="#E3E7EF" if game.theme == "Clair" else "#1E2129",  # Zones secondaires apaisantes
    #     text_color="#1A1A1A" if game.theme == "Clair" else "#EDEDED"
    # )
    #
    # st.markdown(css, unsafe_allow_html=True)
