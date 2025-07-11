import os
import ast
from google import genai
from google.genai import types
from datetime import datetime
import pandas as pd
from geopy.distance import geodesic
from dotenv import load_dotenv
load_dotenv()


class GeospatialGame:
    def __init__(self):
        self.player_name = "Non renseigné"
        self.player_gender = "Non renseigné"
        self.df = self.get_data_from_snowflake()
        self.model = "gemini-2.5-pro"
        self.client = self.get_gemini_connection()
        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.tolerance = 100
        self.player_choice = None
        self.player_score = 0
        self.machine_score = 0
        self.mode = True


    def welcome_message(self):
        message = f"""
        🧠 Concept :\n
        Bienvenue {self.player_name} dans GeoGuessAI, un jeu géospatial passionnant où toi (l’humain) affrontes une IA sur son propre terrain : la connaissance de l’espace.
        Tu peux jouer en mode adresse → coordonnées ou coordonnées → adresse. À chaque tour, c’est à toi de deviner… puis à l’IA. Et le meilleur gagne !\n
        🎯 Objectif du jeu :
        Construire une boucle de jeu interactive où l’utilisateur et l’IA jouent à tour de rôle, chacun essayant de localiser précisément une adresse ou des coordonnées.
        L’objectif est simple : être plus précis que l’IA, cumuler plus de points, et prouver que le cerveau humain sait encore battre les machines ! 🧠⚔️🤖\n
        🕹️ Deux modes de jeu au choix :\n
        🔁 Mode 1 : "Adresse → Coordonnées"\n
        - Une adresse aléatoire est générée.\n
        - Tu dois proposer les coordonnées GPS (latitude / longitude).\n
        - Si la distance entre ta réponse et la vraie position est inférieure à un seuil de tolérance (ex : 100 m), tu gagnes des points.\n
        - Sinon, l’IA tente à son tour de deviner les coordonnées de sa propre adresse aléatoire.\n
        - Même règle, même enjeu.\n
        🧭 Mode 2 : "Coordonnées → Adresse"\n
        Des coordonnées GPS aléatoires sont générées.\n
        Tu dois deviner :\n
        ✅ La commune → +1 point\n
        ✅ Le nom de la voie → +2 points\n
        ✅ Le numéro exact → +3 points\n
        Tu gagnes des points en fonction de ta précision.\n
        Ensuite, l’IA joue aussi, et tente à son tour de répondre à un autre jeu de coordonnées.\n
        
        Bonus : si tu bats l’IA avec plus de précision = bonus combo ! 🎉\n\n
        
        """
        return message

    def start_game(self):
        """
        Permet de lancer le jeu
        :return: le score du joueur et celui de la machine
        """
        # Message de bienvenue
        print(self.welcome_message())

        # # Identification du joueur
        # self.get_player_info()

        # Choix du joueur
        self.player_choice = 2

        if self.player_choice == 2:
            self.mode = False

        # Lancement du jeu
        self.game_tour()

    def get_player_info(self):
        try:
            self.player_name  = input("Veuillez saisir votre prénom/pseudo : ").strip()
            player_gender = ""
            while player_gender not in ["f", "m"]:
                player_gender = input("Veuillez saisir M (si vous avez le genre masculin) ou F (si vous avez le genre féminin) : ").lower().strip()
            if player_gender == "f":
                self.player_gender = "Féminin"
            else:
                self.player_gender = "Masculin"
        except Exception as e:
            print(f"Erreur dans la saisie du nom ou du genre : {e}")


    def choose_game_mode(self):
        """
        Permet au joueur de choisir le mode de jeu au quel il souhaite participer
        :return:le choix du joueur
        """
        try:
            self.player_choice = int(input("Saisi 1 si tu veux jouer avec des coordonnées ou 2 si tu veux jouer avec des adresses : "))
            return self.player_choice
        except ValueError:
            print(f"Veuillez entrer une saisie valide : ")
            self.choose_game_mode()

    def get_data_from_snowflake(self):
        """
        Récupère 10 coordonnées (lat et lon) aléatoire dans la base de données et y ajoute des idenfiants aléatoires
        :return: retourne les coorodnnées en dataframe
        """

        try:
            df = pd.read_csv("../../Data/game_data.csv", sep=";")
            self.df = df.iloc[:, 1:]
            return self.df
        except Exception as e:
            print(f"Erreur de récupération des coordonnées : {e}")

    @staticmethod
    def get_gemini_connection():
        return genai.Client(api_key=os.getenv("API_KEY"))

    @staticmethod
    def get_user_adress():
        while True:
            try:
                commune = input("Veuillez saisir le nom de la commune : ")
                nom_voie = input("Veuillez saisir le nom de la voie : ")
                numero_voie = int(input("Veuillez saisir le numéro de la voie (c'est un entier) : ").strip())
                raw_response = {"commune" : commune, "nom_voie" : nom_voie, "numero_voie": numero_voie}
                return raw_response
            except Exception as e:
                print(f"Erreur dans au moins l'une des saisie : {e}")


    @staticmethod
    def get_user_coordinates():
        while True:
            try:
                latitude = float(input("Veuillez saisir la latitude : "))
                longitude = float(input("Veuillez saisir la longitude : "))
                raw_response = {"latitude" : latitude, "longitude": longitude}
                return raw_response
            except ValueError as e:
                print(f"Erreur dans la saisie (vous devez saisir un nombre réel) : {e}")


    def choose_model_user_response(self, cpt, data=None):
        # Nous nous trouvons dans le cas où le joueur et la machine jouent avec les adresses en entrée
        if self.mode:
            if cpt%2:
                return self.get_user_adress() # La saisie du joueur
            return self.get_model_adress(data) # La réponse du modèle

        # Nous nous trouvons dans le cas où le joueur et la mahcine jouent avec les coordonnées en entrée
        if cpt%2:
            return self.get_user_coordinates() # La saisie du joueur
        return self.get_model_coordinates(data) # La réponse du modèle

    def get_model_adress(self, input):
        """
        Renvoie la l'adresse (nom de la commune et de la voie et numéroe de la voie) fournie par le moddèle Gemini
        :param input: les coordonnées (latitude, longitude)
        :return: liste de l'adresse exacte correspondant à ces coordonnées
        """
        prompt_adress = f"""
        Tu es un expert en géolocalisation et en analyse d'adresses.
        
        Ta mission est de déduire l'adresse complète à partir de coordonnées données, avec la **plus grande précision possible**.
        
        Tu dois impérativement me retourner l'information sous forme d'une **liste Python**, dans cet ordre strict :
        
        ["nom_de_la_commune", "nom_de_la_voie", "numéro_dans_la_voie"]
        
        🛑 Les trois éléments doivent toujours être présents, même si tu dois estimer ou compléter de manière vraisemblable. Ne retourne **aucun autre texte autour**.
        
        Voici l'information à analyser :\n
        Latitude : {input["latitude"]}\n
        Longitude : {input["longitude"]}\n
        """
        print("La machine réflechit actuellement...")
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt_adress],
                config=types.GenerateContentConfig(
                    temperature=0.1
                )
            )
            cleaned_response = response.text.replace("```","").replace("python", "").strip()
            cleaned_response = ast.literal_eval(cleaned_response)
            try:
                numero = int(cleaned_response[2].strip())
                machine_response = {"commune": cleaned_response[0], "nom_voie": cleaned_response[1], "numero_voie": numero}
                return machine_response
            except Exception as e:
                print(f"Erreur dans la transforation du numéro dans la voie {e}")
        except Exception as e:
            print(f"Erreur avec Gemini: {str(e)}")
            return None

    def get_model_coordinates(self, input):
        """
        Renvoie les coordonnées précises d'une lieu à partir de ses adresses (pays, nom de la commune, nom et numéro de la voie)
        :param input: adresse complète
        :return: liste de coordonnées (latitude, longitude)
        """
        prompt_coords = f"""
        Tu es un expert en géolocalisation.

        Ta tâche est de convertir une adresse postale complète en coordonnées GPS précises (latitude et longitude).

        L'adresse fournie est la suivante :
        {input}
        Pays : {input["pays"]}\n
        Commune : {input["commune"]}\n
        Nom de la voie : {input["nom_voie"]}\n
        Numéro de la voie : {input["numero_voie"]}\n

        Tu dois obligatoirement me répondre uniquement par une **liste Python** au format suivant :
        [latitude, longitude]

        📌 Ne retourne rien d’autre que cette liste. Les valeurs doivent être des nombres décimaux au format float.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt_coords],
                config=types.GenerateContentConfig(
                    temperature=0.1
                )
            )
            cleaned_response = response.text.replace("```","").replace("python", "").strip()
            cleaned_response = ast.literal_eval(cleaned_response)
            try:
                latitude, longitude = float(cleaned_response[0]), float(cleaned_response[1])
                machine_response = {"latitude": latitude, "longitude": longitude}
                return machine_response
            except Exception as e:
                print(f"Erreur dans la transforation du numéro dans la voie {e}")
        except Exception as e:
            print(f"Erreur avec Gemini: {str(e)}")
            return None

    def display_current_score(self, score, cpt):
        if cpt % 2:
            self.player_score += score
            print(f"Suuuper ! Vous gagné {score} de plus")
        else:
            self.machine_score += score
            print(f"Coool ! La machine gagne {score} de plus")

    def checked_response(self, raw_responses, cpt):
        """
        Permet de vérifier les informations saisies par le joueur/lamahcine
        :param raw_responses: reponses du joueur/de la mahcine
        :param cpt: tour du joueur/de la machine
        :return: le score du joueur/de la machine
        """
        score = 0
        print(raw_responses)
        try:
            response = self.df.loc[self.df.unique_ids == raw_responses["unique_id"]]
            if self.mode:
                if response["communes"].values[0].lower().strip() == raw_responses["commune"].lower().strip():
                    score = 20
                    self.display_current_score(score, cpt)
                if response["voies"].values[0].lower().strip() == raw_responses["nom_voie"].lower().strip():
                    score = 50
                    self.display_current_score(score, cpt)
                if response["numeros"].values[0] == raw_responses["numero_voie"]:
                    score = 100
                    self.display_current_score(score, cpt)
            else:
                try:
                    distance = geodesic([response["latitude"].values[0], response["longitude"].values[0]], [raw_responses["latitude"], raw_responses["longitude"]]).meters
                    print(f"La précision est de {distance:.2f} mètres \n")
                    accuracies = [0, 15, 50, 100, 200, 500, 1000, 5000, 10000, 15000, 20000]
                    accuracies_reversed = accuracies.copy()
                    accuracies_reversed.reverse()
                    for i in range(len(accuracies)):
                        if self.tolerance - accuracies[i] <= distance < self.tolerance + accuracies[i]:
                            score = accuracies_reversed[i]
                            self.display_current_score(score, cpt)
                            break
                except Exception as e:
                    print(f"Voiiiiiici l'erreur : {e}")
        except Exception as e:
            print(f"Problème de mise à jour du score actuel: {e}")

    def display_final_score(self):
        try:
            final_score = pd.DataFrame({self.player_name : self.player_score, "Machine" : self.machine_score}, index=["Nombre de points"])
            return final_score
        except Exception as e:
            print(f"Erreur dans la récupération scores : {e}")

    def player_tour(self, choosen_data):
        print("-" * 100)
        print("C'est à votre tour de jouer")
        if self.mode:
            lat, lon = choosen_data["latitude"].values[0], choosen_data["longitude"].values[0]
            print(
                f"Voici les coordonnées dont vous devez trouver l'adresse exacte : \nLatitude : {lat} \nLongitude : {lon}\n")
        else:
            commune, nom_voie, num_voie = choosen_data["communes"].values[0], choosen_data["voies"].values[0], \
            choosen_data["numeros"].values[0]
            print(
                f"Voici l'adresse complète dont vous devez deviner les coordonnées exactes : \nCommune : {commune} \nNom de la voie : {nom_voie} \nNuméro de la voie : {num_voie}\n")


    def machine_tour(self, choosen_data):
        print("-" * 100)
        print("C'est au tour de la machine")
        if self.mode:
            lat, lon = choosen_data["latitude"].values[0], choosen_data["longitude"].values[0]
            print(
                f"Voici les coordonnées dont la machine doit trouver l'adresse exacte : \nLatitude : {lat} \nLongitude : {lon}\n")
            data = {"latitude": lat, "longitude": lon}
        else:
            commune, nom_voie, num_voie = choosen_data["communes"].values[0], choosen_data["voies"].values[0], \
            choosen_data["numeros"].values[0]
            print(
                f"Voici l'adresse complète dont la machine doit déviner les coordonnées exactes : \nCommune : {commune} \nNom de la voie : {nom_voie} \nNuméro de la voie : {num_voie}\n")
            data = {"pays": "France", "commune": commune, "nom_voie": nom_voie, "numero_voie": num_voie}
        return data


    def game_tour(self):
        """
        Permet au joueur de jouer de façon iterrative selon le mode de jeu choisi
        :return:
        """
        cpt = 0
        while cpt < 3:
            choosen_coords = self.df.sample(n=1)
            print(choosen_coords)
            if cpt%2:
                self.player_tour(choosen_data=choosen_coords)
                raw_response = self.choose_model_user_response(cpt)
                raw_response["unique_id"] = choosen_coords["unique_ids"].values[0]
                self.checked_response(raw_response, cpt)
                cpt += 1
            else:
                data = self.machine_tour(choosen_data=choosen_coords)
                machine_response = self.choose_model_user_response(cpt, data=data)
                machine_response["unique_id"] = choosen_coords["unique_ids"].values[0]
                self.checked_response(machine_response, cpt)
                cpt += 1

        print(f"Score final \n {self.display_final_score()}")