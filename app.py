import os
import ast
from google import genai
from google.genai import types
from datetime import datetime
import pandas as pd
from geopy.distance import geodesic
from dotenv import load_dotenv
from welcome import display_welcome
from about import display_about
from hall_of_fame import display_hall_of_fame
from setting import _apply_theme_css
from setting import display_settings
load_dotenv()
import streamlit as st


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
        self.current_page = "Settings"

        # Pour les paramètres
        self.ai_delay = 1.0
        self.theme = "Sombre"
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
        """Affiche la barre latérale de navigation"""
        with st.sidebar:
            st.image("../Images/logo.png", width=150)

            # Boutons de navigation
            if st.button("🏠 Accueil"):
                self.current_page = "Home"
                st.rerun()

            if st.button("🏆 Hall of Fame"):
                self.current_page = "Hall of Fame"
                st.rerun()

            if st.button("ℹ️ À propos"):
                self.current_page = "About"
                st.rerun()

            if st.button("⚙️ Paramètres"):
                self.current_page = "Settings"
                st.rerun()


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

    @staticmethod
    def get_gemini_connection():
        """Établit la connexion à l'API Gemini"""
        try:
            return genai.Client(api_key=os.getenv("API_KEY"))
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

        if self.game_mode == "Adresse → Coordonnées":
            self.display_address_to_coords()
        else:
            self.display_coords_to_address()

        st.markdown("---")
        self.display_scoreboard()

    def display_address_to_coords(self):
        """Affiche l'interface pour le mode Adresse → Coordonnées"""
        st.subheader("📍 Adresse à localiser:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Commune:** {self.current_data['communes']}")
            st.markdown(f"**Voie:** {self.current_data['voies']}")
        with col2:
            st.markdown(f"**Numéro:** {self.current_data['numeros']}")

        st.markdown("### Votre réponse")

        with st.form(key="coords_form"):
            # Ajout de on_change=None pour empêcher la soumission automatique
            lat = st.number_input("Latitude:",min_value=-90.0,max_value=90.0,value=0.0,step=0.000001,format="%.6f",key="lat_input",on_change=None)
            lon = st.number_input("Longitude:",min_value=-180.0,max_value=180.0,value=0.0,step=0.000001,format="%.6f",key="lon_input",on_change=None)

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Valider ma réponse",
                                              use_container_width=True,
                                              type="primary")

        if submitted:
            self.check_coords_response({"latitude": lat, "longitude": lon}, is_player=True)
            self.play_machine_turn()
            st.rerun()

    def display_coords_to_address(self):
        """Affiche l'interface pour le mode Coordonnées → Adresse"""
        st.subheader("🌐 Coordonnées à identifier:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Latitude:** {self.current_data['latitude']}")
            st.markdown(f"**Longitude:** {self.current_data['longitude']}")
            st.markdown("### Votre réponse")
            with st.form(key="address_form"):
                commune = st.text_input("Commune:",key="commune_input",on_change=None)
                voie = st.text_input("Nom de la voie:",key="voie_input",on_change=None)
                numero = st.number_input("Numéro:",min_value=1,value=1,key="numero_input",on_change=None)

                # Bouton de soumission avec espacement
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Valider ma réponse",use_container_width=True,type="primary")
        with col2:
            st.map(pd.DataFrame({
                'lat': [self.current_data['latitude']],
                'lon': [self.current_data['longitude']]
            }), zoom=14)
        if submitted:
            self.check_address_response({
                "commune": commune,
                "nom_voie": voie,
                "numero_voie": numero
            }, is_player=True)
            self.play_machine_turn()
            st.rerun()

    def play_machine_turn(self):
        """Fait jouer l'IA et vérifie sa réponse"""
        with st.spinner("L'IA réfléchit..."):
            if self.game_mode == "Adresse → Coordonnées":
                # machine_response = self.get_model_coordinates({
                #     "pays": "France",
                #     "commune": self.current_data["communes"],
                #     "nom_voie": self.current_data["voies"],
                #     "numero_voie": self.current_data["numeros"]
                # })
                machine_response = {
                    "latitude": 45.12454,
                    "longitude": 1.54887
                }
                if machine_response:
                    self.check_coords_response(machine_response, is_player=False)
            else:
                # machine_response = self.get_model_adress({
                #     "latitude": self.current_data["latitude"],
                #     "longitude": self.current_data["longitude"]
                # })

                machine_response = {"commune": "Alexandre", "nom_voie": "30", "numero_voie": "Data scientist"}
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

    def calculate_points_from_distance(self, distance):
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
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
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
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
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
        """Affiche le tableau des scores"""
        st.subheader("📊 Scores")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"👤 {self.player_name}", self.player_score)
        with col2:
            st.metric("👾 Machine", self.machine_score)

        # Afficher les résultats du dernier tour si disponibles
        if 'last_player_score' in st.session_state:
            st.info(f"Dernier tour: Vous avez marqué {st.session_state.last_player_score} points")
        if 'last_machine_score' in st.session_state:
            st.info(f"Dernier tour: La machine a marqué {st.session_state.last_machine_score} points")

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
        if "theme" in st.query_params:
            theme_param = st.query_params.theme
            if theme_param in ["light", "dark"]:
                self.theme = "Clair" if theme_param == "light" else "Sombre"

        _apply_theme_css(self)
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

