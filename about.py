import streamlit as st

def display_about():
    """Affiche la page À propos"""
    st.title("À propos de GeoGuessAI")

    st.markdown("""
    ### 🌍 GeoGuessAI - Duel Géospatial

    **Version:** 1.0  
    **Auteur:** Marcel Assie 
    **Date:** 2025  

    ### 📚 Description
    GeoGuessAI est un jeu qui vous met au défi de rivaliser avec une intelligence artificielle 
    dans des épreuves de géolocalisation. Testez vos connaissances géographiques et voyez 
    si vous pouvez battre l'IA !

    ### 🛠 Technologies utilisées
    - Python
    - Streamlit
    - Google Gemini API
    - Pandas
    - Geopy

    ### 📝 Licence
    Ce projet est sous licence MIT.
    """)