import streamlit as st
import pandas as pd

def display_hall_of_fame():
    """Affiche le Hall of Fame"""
    st.title("🏆 Hall of Fame")

    st.markdown("""
    ### Les meilleurs joueurs

    Voici les scores les plus impressionnants enregistrés dans notre jeu :
    """)

    # Exemple de données - vous pourriez charger cela depuis un fichier
    hall_of_fame_data = [
        {"name": "Marie", "score": 2450, "date": "2025-06-15"},
        {"name": "Pierre", "score": 1980, "date": "2025-06-14"},
        {"name": "Sophie", "score": 1850, "date": "2025-06-12"},
        {"name": "Jean", "score": 1720, "date": "2025-06-10"},
        {"name": "Lucie", "score": 1650, "date": "2025-06-08"},
    ]

    st.table(pd.DataFrame(hall_of_fame_data))