import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np


def get_medal_emoji(rank):
    """Retourne l'emoji de médaille selon le rang"""
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else:
        return f"#{rank}"


def get_rank_color(rank):
    """Retourne la couleur selon le rang"""
    if rank == 1:
        return "#FFD700"  # Or
    elif rank == 2:
        return "#C0C0C0"  # Argent
    elif rank == 3:
        return "#CD7F32"  # Bronze
    else:
        return "#4A90E2"  # Bleu


def create_animated_score_chart(data):
    """Crée un graphique animé des scores"""
    fig = go.Figure()

    # Ajouter les barres avec animation
    fig.add_trace(go.Bar(
        x=[f"{get_medal_emoji(i + 1)} {row['name']}" for i, row in enumerate(data)],
        y=[row['score'] for row in data],
        marker=dict(
            color=[get_rank_color(i + 1) for i in range(len(data))],
            line=dict(color='rgba(0,0,0,0.2)', width=2)
        ),
        text=[f"{row['score']} pts" for row in data],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Score: %{y} pts<br>Date: %{customdata}<extra></extra>',
        customdata=[row['date'] for row in data]
    ))

    fig.update_layout(
        title={
            'text': 'Classement des Scores',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2E86AB'}
        },
        xaxis_title="Joueurs",
        yaxis_title="Score",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=500,
        margin=dict(t=80, b=40, l=40, r=40)
    )

    # Ajouter des effets visuels
    fig.update_xaxes(showgrid=False, tickangle=45)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')

    return fig


def create_progress_timeline(data):
    """Crée une timeline des progrès"""
    dates = [datetime.strptime(row['date'], '%Y-%m-%d') for row in data]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=[row['score'] for row in data],
        mode='lines+markers',
        name='Évolution des scores',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(
            size=12,
            color=[get_rank_color(i + 1) for i in range(len(data))],
            line=dict(color='white', width=2)
        ),
        text=[f"{row['name']}: {row['score']} pts" for row in data],
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Score: %{y} pts<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': 'Timeline des Performances',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#2E86AB'}
        },
        xaxis_title="Date",
        yaxis_title="Score",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig


def display_hall_of_fame():
    """Affiche le Hall of Fame avec une interface moderne et interactive"""

    # Configuration de la page
    st.set_page_config(layout="wide")

    # En-tête avec animation CSS
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 30px;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(102, 126, 234, 0.5); }
        to { text-shadow: 0 0 30px rgba(118, 75, 162, 0.8); }
    }

    .champion-card {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px 0;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    .podium-container {
        display: flex;
        justify-content: center;
        align-items: end;
        margin: 30px 0;
        gap: 20px;
    }

    .podium-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        font-weight: bold;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }

    .podium-step:hover {
        transform: translateY(-5px);
    }

    .podium-1 { height: 120px; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); }
    .podium-2 { height: 100px; background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%); }
    .podium-3 { height: 80px; background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%); }
    </style>
    """, unsafe_allow_html=True)

    # Titre principal
    st.markdown('<h1 class="main-title">🏆 Hall of Fame 🏆</h1>', unsafe_allow_html=True)

    # Données d'exemple enrichies
    hall_of_fame_data = [
        {"name": "Sarah", "score": 2450, "date": "2025-06-15", "games": 45, "accuracy": 89.5, "country": "🇫🇷"},
        {"name": "Imane", "score": 1980, "date": "2025-06-14", "games": 38, "accuracy": 85.2, "country": "🇧🇪"},
        {"name": "Celia", "score": 1850, "date": "2025-06-12", "games": 42, "accuracy": 82.1, "country": "🇫🇷"},
        {"name": "Marcel", "score": 1720, "date": "2025-06-10", "games": 35, "accuracy": 78.9, "country": "🇨🇦"},
        {"name": "Laura Lee", "score": 1650, "date": "2025-06-08", "games": 40, "accuracy": 76.3, "country": "🇫🇷"},
        {"name": "Yohan", "score": 1580, "date": "2025-06-07", "games": 33, "accuracy": 74.8, "country": "🇬🇧"},
        {"name": "Gaëlle", "score": 1520, "date": "2025-06-06", "games": 37, "accuracy": 72.5, "country": "🇩🇪"},
        {"name": "Ibrahima", "score": 1480, "date": "2025-06-05", "games": 29, "accuracy": 71.2, "country": "🇪🇸"},
    ]

    # Champion actuel
    champion = hall_of_fame_data[0]
    st.markdown(f"""
    <div class="champion-card">
        <h2>👑 Champion Actuel 👑</h2>
        <h1>{champion['country']} {champion['name']}</h1>
        <h2>{champion['score']} points</h2>
        <p>🎯 Précision: {champion['accuracy']}% | 🎮 Parties: {champion['games']} | 📅 {champion['date']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Podium des 3 premiers
    st.markdown("### Podium des Champions")

    podium_cols = st.columns([1, 2, 1.5, 1])

    with podium_cols[1]:
        st.markdown(f"""
        <div class="podium-step podium-2">
            <h4>🥈 {hall_of_fame_data[1]['country']} {hall_of_fame_data[1]['name']}</h4>
        </div>
        """, unsafe_allow_html=True)

    with podium_cols[2]:
        st.markdown(f"""
        <div class="podium-step podium-1">
            <h4>🥇 {hall_of_fame_data[0]['country']} {hall_of_fame_data[0]['name']}</h4>
        </div>
        """, unsafe_allow_html=True)

    with podium_cols[3]:
        st.markdown(f"""
        <div class="podium-step podium-3">
            <h4>🥉 {hall_of_fame_data[2]['country']} {hall_of_fame_data[2]['name']}</h4>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Statistiques globales
    st.markdown("### Statistiques Globales")

    stats_cols = st.columns(4)

    with stats_cols[0]:
        st.markdown(f"""
        <div class="stat-card">
            <h3>🎯</h3>
            <h2>{len(hall_of_fame_data)}</h2>
            <p>Joueurs Actifs</p>
        </div>
        """, unsafe_allow_html=True)

    with stats_cols[1]:
        avg_score = np.mean([d['score'] for d in hall_of_fame_data])
        st.markdown(f"""
        <div class="stat-card">
            <h3>📈</h3>
            <h2>{avg_score:.0f}</h2>
            <p>Score Moyen</p>
        </div>
        """, unsafe_allow_html=True)

    with stats_cols[2]:
        total_games = sum([d['games'] for d in hall_of_fame_data])
        st.markdown(f"""
        <div class="stat-card">
            <h3>🎮</h3>
            <h2>{total_games}</h2>
            <p>Parties Jouées</p>
        </div>
        """, unsafe_allow_html=True)

    with stats_cols[3]:
        avg_accuracy = np.mean([d['accuracy'] for d in hall_of_fame_data])
        st.markdown(f"""
        <div class="stat-card">
            <h3>🎯</h3>
            <h2>{avg_accuracy:.1f}%</h2>
            <p>Précision Moyenne</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Graphiques interactifs
    chart_cols = st.columns(2)

    with chart_cols[0]:
        fig_bar = create_animated_score_chart(hall_of_fame_data[:5])
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_cols[1]:
        fig_timeline = create_progress_timeline(hall_of_fame_data[:5])
        st.plotly_chart(fig_timeline, use_container_width=True)

    st.markdown("---")

    # Tableau détaillé avec style
    st.markdown("### Classement Détaillé")

    # Création du DataFrame avec des colonnes formatées
    df = pd.DataFrame(hall_of_fame_data)
    df['Rang'] = [get_medal_emoji(i + 1) for i in range(len(df))]
    df['Joueur'] = df['country'] + ' ' + df['name']
    df['Score'] = df['score'].apply(lambda x: f"{x:,} pts")
    df['Précision'] = df['accuracy'].apply(lambda x: f"{x}%")
    df['Parties'] = df['games'].apply(lambda x: f"{x} parties")
    df['Date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y')

    # Affichage du tableau stylisé
    display_df = df[['Rang', 'Joueur', 'Score', 'Précision', 'Parties', 'Date']]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rang": st.column_config.TextColumn("🏆 Rang", width="small"),
            "Joueur": st.column_config.TextColumn("👤 Joueur", width="medium"),
            "Score": st.column_config.TextColumn("⭐ Score", width="small"),
            "Précision": st.column_config.TextColumn("🎯 Précision", width="small"),
            "Parties": st.column_config.TextColumn("🎮 Parties", width="small"),
            "Date": st.column_config.TextColumn("📅 Date", width="small"),
        }
    )

    # Bouton de retour avec style
    st.markdown("---")



    # Footer avec animation
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
        <h3>🌟 Rejoignez la Légende ! 🌟</h3>
        <p>Montrez vos compétences géographiques et gravez votre nom dans l'histoire !</p>
    </div>
    """, unsafe_allow_html=True)