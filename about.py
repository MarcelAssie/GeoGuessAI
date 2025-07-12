import streamlit as st

def display_about():
    """Affiche la page À propos professionnelle et dynamique de GeoGuessAI"""
    st.title("À propos de GeoGuessAI 🌍")

    st.markdown("""
    ## Présentation du projet

    **GeoGuessAI** est un jeu géospatial innovant où l’intelligence humaine affronte une intelligence artificielle dans des défis de localisation.  
    Le joueur et l’IA jouent chacun leur tour pour deviner une adresse à partir de coordonnées GPS ou inversement.  
    L’objectif : être plus précis, plus rapide et plus stratégique que la machine.

    Ce projet fusionne **données spatiales**, **intelligence artificielle** et **expérience utilisateur interactive** pour offrir une approche ludique et pédagogique à la géolocalisation.

    ---

    ## Auteur

    **Marcel Assie**  
    Étudiant-ingénieur en Geo Data Sceince à l’ENSG, passionné de géodata, IA, et innovation pédagogique.  
    GeoGuessAI est né de sa volonté de créer un outil à la fois **fun**, **technique** et **inspirant**, où l’on peut apprendre en jouant avec les données.

    Son objectif : promouvoir l’usage des technologies spatiales de façon accessible, interactive et intelligente 🚀

    ---

    ## Technologies utilisées

    Ce projet repose principalement sur **Python** et les bibliothèques suivantes :

    - **Streamlit** pour l’interface web
    - **Geopy** pour le calcul des distances géographiques
    - **OpenAI / Gemini API** pour les réponses IA contextuelles
    - **Pandas** pour la gestion des données
    - **Folium** (en cours d’intégration) pour les cartes interactives

    Données issues de sources ouvertes comme **OpenStreetMap**, **BAN**, ou des fichiers CSV locaux.

    ---

    ## État actuel du projet – *Version 1.0*

    - Deux modes de jeu :  
      - **Adresse → Coordonnées**  
      - **Coordonnées → Adresse (commune, voie, numéro)**
    - Jouabilité tour par tour humain / IA 🧠⚔️👾 
    - Attribution de points selon la précision des réponses  
    - Données chargées localement (fichier CSV de test)  
    - Interface fonctionnelle avec Streamlit

    Le projet est **jouable localement** en environnement Python dès cette version.

    ---

    ## Perspectives d’évolution

    Plusieurs améliorations sont prévues pour les versions futures :

    - Connexion à des **APIs d’adresses en temps réel** (ex. BAN, OSM Nominatim)
    - Intégration de **cartes interactives** pour visualiser les réponses 
    - Tableau de scores dynamique et multi-joueurs
    - Enrichissement des **réponses IA** avec raisonnement contextuel (__on verra bien haha__)
    - Mode **arcade** : manches chronométrées et niveaux de difficulté
    - Déploiement en ligne ou en application mobile

    L’ambition est claire : faire de GeoGuessAI une **plateforme ludique de référence** pour découvrir, apprendre et s’amuser avec la géodata.

    ---

    ## Licence

    Ce projet est sous licence **MIT**.  
    Vous êtes libre de l’utiliser, l’adapter et le diffuser, à condition de respecter les termes de la licence et de créditer l’auteur.

    ---

    ## Remerciements

    Merci à toutes les personnes qui testent, proposent des idées, ou s’intéressent à ce projet.  
    GeoGuessAI est un **terrain d’expérimentation et de partage** autour de la géomatique et de l’intelligence artificielle.

    Pour toute suggestion, bug ou collaboration, n’hésitez pas à me contacter.

    ---
    """)

