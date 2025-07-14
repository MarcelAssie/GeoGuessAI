import ast
import os
import google.generativeai as genai
from datetime import datetime
import pandas as pd
from geopy.distance import geodesic
from dotenv import load_dotenv
from welcome import display_welcome
from about import display_about
from hall_of_fame import display_hall_of_fame
from setting import display_settings
load_dotenv()
import streamlit as st
from utils import display_address_to_coords, display_coords_to_address

class GeospatialGame:
    def __init__(self):
        """Initialise le jeu avec les paramètres par défaut"""
        self.player_name = "Joueur"
        self.player_gender = "Non renseigné"
        self.df = self.load_data()
        self.model = "gemini-2.5-flash"
        self.client = self.get_gemini_connection()
        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.tolerance = 100
        self.player_score = 0
        self.machine_score = 0
        self.current_round = 0
        self.max_rounds = 3
        self.game_mode = None
        self.current_data = None
        self.game_history = []
        self.current_page = "Home"

        # Pour les paramètres
        self.ai_delay = 1.0
        self.theme = "Auto"
        self.accent_color = "#00C0F2"
        self.animation_speed = 1.0
        self.enable_sound = True
        self.enable_bonus = True
        self.enable_debug = False
        self.allow_retry = True

        # Configuration de la page Streamlit
        st.set_page_config(
            page_title="GeoGuessAI",
            page_icon="🌍",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def display_home(self):
        """Affiche la page d'accueil principale"""
        if self.current_round == 0:
            display_welcome(self)
        elif self.current_round <= self.max_rounds:
            self.display_round()
        else:
            self.display_final_results()

    def display_sidebar(self):
        """Affiche une barre latérale stylisée avec navigation et informations"""
        with st.sidebar:
            st.markdown("""
            <style>
                .sidebar .sidebar-content {
                    background: linear-gradient(180deg, #2c3e50 0%, #1a1a2e 100%);
                    color: white;
                    padding: 2rem 1rem;
                }
                .sidebar-logo {
                    text-align: center;
                    margin-bottom: 2rem;
                    margin-top:0;
                    animation: fadeIn 1s ease-in-out;
                }
            </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
            st.image("../Images/logo2.png", width=150)
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button("Accueil", key="home_btn"):
                self.current_page = "Home"
                st.rerun()

            if st.button("Hall of Fame", key="hof_btn"):
                self.current_page = "Hall of Fame"
                st.rerun()

            if st.button("À propos", key="about_btn"):
                self.current_page = "About"
                st.rerun()

            if st.button("Paramètres", key="settings_btn"):
                self.current_page = "Settings"
                st.rerun()


            # Pied de page minimaliste
            st.markdown("""
            <div style="margin-top: 5rem; text-align: center; font-size: 0.8rem; color: #888;">
                GeoGuessAI v1.0.0<br>© Copyright <br>2025 Marcel Assie - GeoAI Engineer
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def load_data():
        """Charge les données de jeu depuis un fichier CSV"""
        try:
            # Chemin relatif adapté pour Streamlit
            df = pd.read_csv("../Data/game_data.csv", sep=";")
            return df.iloc[:, 1:]
        except Exception as e:
            st.error(f"Erreur de chargement des données: {e}")
            return pd.DataFrame()

    def get_gemini_connection(self):
        """Établit la connexion à l'API Gemini"""
        try:
            # return genai.configure(api_key=os.getenv("API_KEY"))
            genai.configure(api_key=os.getenv("API_KEY"))
            return genai.GenerativeModel(model_name=self.model)
        except Exception as e:
            st.error(f"Erreur de connexion à Gemini: {e}")
            return None



    def start_round(self):
        """Prépare une nouvelle manche de jeu"""
        if len(self.df) == 0:
            st.error("Aucune donnée disponible pour jouer.")
            return

        self.current_data = self.df.sample(n=1).iloc[0]

        if self.game_mode == "Adresse → Coordonnées":
            self.game_history.append({
                "round": self.current_round,
                "type": "Adresse → Coordonnées",
                "data": {
                    "commune": self.current_data["communes"],
                    "voie": self.current_data["voies"],
                    "numero": self.current_data["numeros"]
                }
            })
        else:
            self.game_history.append({
                "round": self.current_round,
                "type": "Coordonnées → Adresse",
                "data": {
                    "latitude": self.current_data["latitude"],
                    "longitude": self.current_data["longitude"]
                }
            })

    def display_round(self):
        """Affiche l'interface pour la manche en cours"""
        if self.current_data is None:
            return

        st.header(f"Manche {self.current_round} sur {self.max_rounds}")

        # Afficher le scoreboard en premier (sera positionné en haut à droite par le CSS)
        self.display_scoreboard()

        if self.game_mode == "Adresse → Coordonnées":
            display_address_to_coords(self)
        else:
            display_coords_to_address(self)

        st.markdown("---")

    def play_machine_turn(self):
        """Fait jouer l'IA et vérifie sa réponse"""
        with st.spinner("Patientez... La machine réfléchit..."):
            if self.game_mode == "Adresse → Coordonnées":
                machine_response = self.get_model_coordinates({
                    "pays": "France",
                    "commune": self.current_data["communes"],
                    "nom_voie": self.current_data["voies"],
                    "numero_voie": self.current_data["numeros"]
                })
                # machine_response = {
                #     "latitude": 45.12454,
                #     "longitude": 1.54887
                # }
                if machine_response:
                    self.check_coords_response(machine_response, is_player=False)
            else:
                machine_response = self.get_model_adress({
                    "latitude": self.current_data["latitude"],
                    "longitude": self.current_data["longitude"]
                })

                # machine_response = {"commune": "Alexandre", "nom_voie": "30", "numero_voie": "Data scientist"}
                if machine_response:
                    self.check_address_response(machine_response, is_player=False)

        # Préparer la prochaine manche ou terminer le jeu
        self.current_round += 1
        if self.current_round <= self.max_rounds:
            self.start_round()
        else:
            self.display_final_results()

    def check_coords_response(self, response, is_player=True):
        """Vérifie la réponse pour le mode Adresse → Coordonnées"""
        try:
            true_coords = (self.current_data["latitude"], self.current_data["longitude"])
            player_coords = (response["latitude"], response["longitude"])

            distance = geodesic(true_coords, player_coords).meters
            st.session_state.last_distance = distance

            # Calcul des points selon la précision
            points = self.calculate_points_from_distance(distance)

            if is_player:
                self.player_score += points
                st.session_state.last_player_score = points
            else:
                self.machine_score += points
                st.session_state.last_machine_score = points

        except Exception as e:
            st.error(f"Erreur lors de la vérification: {e}")

    @staticmethod
    def calculate_points_from_distance(distance):
        """Calcule les points en fonction de la distance (en mètres)"""
        if distance < 5:
            return 1500  # Cas exceptionnel ultra-précis
        elif distance < 20:
            return 1000
        elif distance < 50:
            return 700
        elif distance < 100:
            return 500
        elif distance < 250:
            return 300
        elif distance < 500:
            return 200
        elif distance < 1000:
            return 120
        elif distance < 2000:
            return 80
        elif distance < 5000:
            return 40
        elif distance < 10000:
            return 20
        elif distance < 20000:
            return 10
        elif distance < 50000:
            return 5
        else:
            return 0

    def check_address_response(self, response, is_player=True):
        """Vérifie la réponse pour le mode Coordonnées → Adresse"""
        points = 0

        # Vérification de la commune
        if response["commune"].lower().strip() == self.current_data["communes"].lower().strip():
            points += 20

        # Vérification de la voie
        if response["nom_voie"].lower().strip() == self.current_data["voies"].lower().strip():
            points += 50

        # Vérification du numéro
        if response["numero_voie"] == self.current_data["numeros"]:
            points += 100

        if is_player:
            self.player_score += points
            st.session_state.last_player_score = points
        else:
            self.machine_score += points
            st.session_state.last_machine_score = points

    def get_model_adress(self, input_coords):
        """Demande à Gemini de trouver l'adresse correspondant aux coordonnées"""
        prompt = f"""
        Tu es un expert en géolocalisation et en analyse d'adresses.
        
        Ta mission est de déduire l'adresse complète à partir de coordonnées données, avec la plus grande précision possible.
        
        Tu dois impérativement me retourner l'information sous forme d'une liste Python, dans cet ordre strict :
        
        ["nom_de_la_commune", "nom_de_la_voie", "numéro_dans_la_voie"]
        
        Voici les coodonnées à analyser :
        Latitude: {input_coords['latitude']}
        Longitude: {input_coords['longitude']}

        🛑 Les trois éléments doivent toujours être présents, même si tu dois estimer ou compléter de manière vraisemblable. Ne retourne aucun autre texte autour.
        ["nom_commune", "nom_voie", "numéro_voie"]
        """

        try:
            # model = genai.GenerativeModel(model_name="gemini-pro")
            #
            # # 3. Génération de contenu
            # response = model = self.client.models.generate_content(
            #     model=self.model,
            #     contents=[prompt],
            #     config=types.GenerateContentConfig(
            #         temperature=0.1
            #     )
            # )


            # 3. Génération de contenu
            response = self.client.generate_content(
                contents=[prompt],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1
                )
            )

            cleaned = response.text.replace("```", "").replace("python", "").strip()
            result = ast.literal_eval(cleaned)

            return {
                "commune": result[0],
                "nom_voie": result[1],
                "numero_voie": int(result[2]) if result[2].isdigit() else 0
            }
        except Exception as e:
            st.error(f"Erreur Gemini: {e}")
            return None

    def get_model_coordinates(self, input_address):
        """Demande à Gemini de trouver les coordonnées correspondant à l'adresse"""
        prompt = f"""
        Tu es un expert en géolocalisation.

        Ta tâche est de convertir une adresse postale complète en coordonnées GPS précises (latitude et longitude).

        L'adresse fournie est la suivante :
        Pays: France
        Commune: {input_address['commune']}
        Voie: {input_address['nom_voie']}
        Numéro: {input_address['numero_voie']}

        Tu dois obligatoirement me répondre uniquement par une liste Python au format suivant :
        [latitude, longitude]

        Ne retourne rien d’autre que cette liste. Les valeurs doivent être des nombres décimaux au format float.
        """

        try:
            # response = self.client.models.generate_content(
            #     model=self.model,
            #     contents=[prompt],
            #     config=types.GenerateContentConfig(
            #         temperature=0.1
            #     )
            # )
            response = self.client.generate_content(
                contents=[prompt],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1
                )
            )

            cleaned = response.text.replace("```", "").replace("python", "").strip()
            result = ast.literal_eval(cleaned)
            return {
                "latitude": float(result[0]),
                "longitude": float(result[1])
            }
        except Exception as e:
            st.error(f"Erreur Gemini: {e}")
            return None

    def display_scoreboard(self):
        """Affiche le tableau des scores sous forme de popup stylé en haut à droite"""
        # Style CSS personnalisé
        st.markdown("""
        <style>
            .score-popup {
                position: fixed;
                top: 42px;
                right: 10px;
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                z-index: 1000;
                border-left: 5px solid #4CAF50;
                animation: slideIn 0.5s ease-in-out;
                max-width: 300px;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .score-title {
                font-size: 1.2em;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }
            .score-item {
                display: flex;
                justify-content: space-between;
                margin: 8px 0;
            }
            .player-name {
                font-weight: bold;
            }
            .player-score {
                background-color: #f0f2f6;
                padding: 2px 8px;
                border-radius: 12px;
                font-weight: bold;
                color: #4CAF50;
            }
            .last-round {
                margin-top: 10px;
                font-size: 0.9em;
                color: #666;
                border-top: 1px dashed #eee;
                padding-top: 8px;
            }
        </style>
        """, unsafe_allow_html=True)

        # Construction du HTML de manière plus propre
        score_html = [
            '<div class="score-popup">',
            '<div class="score-title">📊 Scores</div>',
            f'<div class="score-item"><span class="player-name">👤 {self.player_name}</span><span class="player-score">{self.player_score} pts</span></div>',
            f'<div class="score-item"><span class="player-name">👾 Machine</span><span class="player-score">{self.machine_score} pts</span></div>'
        ]

        # Ajouter les résultats du dernier tour si disponibles
        if 'last_player_score' in st.session_state or 'last_machine_score' in st.session_state:
            score_html.append('<div class="last-round">')
            if 'last_player_score' in st.session_state:
                score_html.append(f'<div>Vous: +{st.session_state.last_player_score} pts</div>')
            if 'last_machine_score' in st.session_state:
                score_html.append(f'<div>Machine: +{st.session_state.last_machine_score} pts</div>')
            score_html.append('</div>')

        score_html.append('</div>')

        # Affichage final
        st.markdown(''.join(score_html), unsafe_allow_html=True)

    def display_final_results(self):
        """Affiche les résultats finaux du jeu"""
        st.balloons()
        st.title("🏁 Résultats finaux")

        # Déterminer le gagnant
        if self.player_score > self.machine_score:
            st.success(f"🎉 Félicitations {self.player_name}, vous avez gagné !")
        elif self.player_score < self.machine_score:
            st.error("😢 La machine a gagné cette fois...")
        else:
            st.warning("🤝 Égalité parfaite !")

        # Afficher les scores finaux
        st.subheader("Scores finaux")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"👤 {self.player_name}", self.player_score)
        with col2:
            st.metric("👾 Machine", self.machine_score)

        # Bouton pour rejouer - Version corrigée
        if st.button("Rejouer 🔄", type="primary"):
            # Réinitialisation propre des variables de session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    def run(self):
        """Lance l'application Streamlit avec la navigation"""
        # if "theme" in st.query_params:
        #     theme_param = st.query_params.theme
        #     if theme_param in ["light", "dark"]:
        #         self.theme = "Clair" if theme_param == "light" else "Sombre"
        #
        # _apply_theme_css(self)
            # 2. Appliquer le CSS personnalisé si nécessaire
        self.display_sidebar()

        # Gestion de l'affichage en fonction de la page courante
        if self.current_page == "Home":
            self.display_home()
        elif self.current_page == "Hall of Fame":
            display_hall_of_fame()
        elif self.current_page == "About":
            display_about()
        elif self.current_page == "Settings":
            display_settings(self)

