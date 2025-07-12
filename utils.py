from math import radians, sin, cos, sqrt, atan2
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

def calculate_distance(coord1, coord2):
    """Calcule la distance en km entre deux points géographiques (lat, lon)"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Conversion en radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Différences de coordonnées
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Formule de Haversine
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Rayon de la Terre en km (6371)
    distance = 6371 * c
    return distance

def display_address_to_coords(game):
    """Affiche l'interface pour le mode Adresse → Coordonnées"""
    st.subheader("📍 Adresse à localiser:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Commune:** {game.current_data['communes']}")
    with col2:
        st.markdown(f"**Nom de la voie:** {game.current_data['voies']}")
    with col3:
        st.markdown(f"**Numéro de la voie :** {game.current_data['numeros']}")


    col4, col5 = st.columns([1,3])
    with col4:
        st.markdown("### Votre réponse")
        with st.form(key="coords_form"):
            lat = st.number_input("Latitude:",min_value=-90.0,max_value=90.0,value=0.0,step=0.000001,format="%.6f",key="lat_input",on_change=None)
            lon = st.number_input("Longitude:",min_value=-180.0,max_value=180.0,value=0.0,step=0.000001,format="%.6f",key="lon_input",on_change=None)

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Valider ma réponse",
                                              use_container_width=True,
                                              type="primary")
            with st.container(border=True):
                # Calcul de la distance entre Paris et le lieu exact
                paris_coords = (48.8566, 2.3522)
                target_coords = (game.current_data['latitude'], game.current_data['longitude'])
                distance = geodesic(paris_coords, target_coords).meters

                st.markdown(f"**Distance depuis Paris:** {distance/1000:.2f} km")
                st.markdown(f"**Coordonnées de Paris:** {paris_coords[0]:.6f}, {paris_coords[1]:.6f}")

    with st.container(border=True):
        with col5:

            m = folium.Map(location=[46.227638, 2.213749], zoom_start=5)

            folium.Marker([game.current_data['latitude'], game.current_data['longitude']], tooltip="Je suis ici",icon=folium.Icon(color='green')).add_to(m)

            folium.CircleMarker(location=[game.current_data['latitude'], game.current_data['longitude']],radius=50,color="cornflowerblue",stroke=False,fill=True,fill_opacity=0.7,opacity=1).add_to(m)

            st_folium(m, width=1200, height=500)

    if submitted:
        game.check_coords_response({"latitude": lat, "longitude": lon}, is_player=True)
        game.play_machine_turn()
        st.rerun()

def display_coords_to_address(game):
    """Affiche l'interface pour le mode Coordonnées → Adresse"""
    st.subheader("🌐 Coordonnées à identifier:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Latitude:** {game.current_data['latitude']}")
        st.markdown(f"**Longitude:** {game.current_data['longitude']}")
        st.markdown("### Votre réponse")
        with st.form(key="address_form"):
            commune = st.text_input("Commune:", key="commune_input")
            voie = st.text_input("Nom de la voie:", key="voie_input")
            numero = st.number_input("Numéro:", min_value=1, value=1, key="numero_input")

            # Bouton de soumission avec espacement
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Valider ma réponse",
                                              use_container_width=True,
                                              type="primary")

    with col2:
        # Crée une carte figée (non interactive)
        m = folium.Map(location=[game.current_data['latitude'], game.current_data['longitude']], zoom_start=8, zoom_control=False, dragging=False, touchZoom=False, scrollWheelZoom=False, doubleClickZoom=False, boxZoom=False, keyboard=False)
        folium.Marker(
            [game.current_data['latitude'], game.current_data['longitude']],
            popup="Lieu à trouver",
            tooltip="Lieu à trouver"
        ).add_to(m)

        # Affiche la carte avec des paramètres qui la rendent statique
        st_folium(m, width=1200, height=500)

    if submitted:
        game.check_address_response({
            "commune": commune,
            "nom_voie": voie,
            "numero_voie": numero
        }, is_player=True)
        game.play_machine_turn()
        st.rerun()
