# 🌍 GeoGuessAI – The Human vs AI Geospatial Challenge 

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![AI-Powered](https://img.shields.io/badge/AI-Gemini%202.5%20Pro-ff9800?logo=google)](https://deepmind.google/technologies/gemini/)
[![GeoData](https://img.shields.io/badge/Data-GeoJSON%2FCSV-lightgrey?logo=openstreetmap)](https://www.openstreetmap.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app/)

> 🕹️ A Python-powered geolocation game where a **human competes with an AI** in guessing locations from either coordinates or addresses.
> Built to explore the frontier between **human intuition** and **machine intelligence**, while having fun with real geospatial data.

---

## Concept

**GeoGuessAI** is a next-gen geolocation challenge game blending **AI**, **spatial data**, and **interactive gameplay**.
The goal? Outguess the AI, earn points through precision, and prove that human geographical intuition still matters!

### Game Modes

* **Address → Coordinates**
  Given an address, try to guess the exact **latitude and longitude**.
* **Coordinates → Address**
  From a pair of GPS coordinates, identify the **city**, **street**, and **house number**.

Every round alternates between the **player** and the **AI (Gemini 2.5 Pro)**.
Points are awarded based on **accuracy**, with partial credit for close guesses.

---

## Motivation

> “I built GeoGuessAI to explore the fusion of geodata, machine learning, and user experience — a fun and educational way to experiment with spatial intelligence.”
> — *Marcel Assie, Creator*

This project is part of an ongoing mission to make **spatial technologies accessible, inspiring, and engaging**, especially for students, data enthusiasts, and AI practitioners.

---

## Features

* Terminal + Web interface (Streamlit)
* Turn-based play: human vs AI
* Score calculated by spatial distance (Haversine)
* Uses real-world data (OpenStreetMap, BAN)
* Gemini-powered predictions (via Google GenAI)
* Local CSV input + easy extensibility
* Score display + optional visual feedback with Folium

---

## Screenshots / Preview

> *(You can add visuals here in your GitHub later)*

```
Round 2: Human's Turn
Guess the coordinates of: 25 Rue Victor Hugo, Paris

Latitude: 48.8529
Longitude: 2.3476

Example : Precision: 87.5 meters → You earned +200 points!
```

---

## Getting Started

### Requirements

* Python 3.10+
* Google Gemini API key
* `game_data.csv` file (see format below)

### ⚙️ Installation

```bash
git clone https://github.com/MarcelAssie/GeoGuessAI.git
pip install -r requirements.txt
```

Create a `.env` file at the root:

```env
API_KEY=your_google_gemini_api_key
```

To run the **Streamlit interface**:

```bash
streamlit run main.py
```

---

## Dataset Format

> Stored in `Data/game_data.csv`

```
unique_ids;latitude;longitude;communes;voies;numeros
id_001;48.8566;2.3522;Paris;Rue de Rivoli;25
...
```

You can generate this from:

* OpenStreetMap
* Base Adresse Nationale (BAN)
* Your own local data

---

## AI Prompting

The AI is prompted with **structured instructions** for strict parsing:

### Coordinate to Address:

```python
["Paris", "Rue de Rivoli", 25]
```

### Address to Coordinate:

```python
[48.8566, 2.3522]
```

Strict formats ensure smooth validation and fair comparison with human inputs.

---

## Tech Stack

| Component         | Description                  |
| ----------------- | ---------------------------- |
| Python 3.10+      | Core language                |
| Streamlit         | Web interface (optional)     |
| Geopy             | Distance calculations        |
| Pandas            | Data handling                |
| Folium            | Map visualization (optional) |
| Google Gemini API | Generative AI responses      |
| dotenv            | API key management           |

---

## What’s Next?

Planned enhancements for future versions:

* Integration with **live geocoding APIs** (Nominatim, Google Maps)
* Map feedback using **Folium + Leaflet**
* Multiplayer or **AI vs AI**
* **Arcade mode** with difficulty scaling and time limits
* Configurable interface: tolerance, data source, themes
* Leaderboards and score history
* Mobile app deployment (React Native or Flutter)

---

## License

This project is licensed under the **[MIT License](LICENSE)**.
Feel free to reuse, modify, and redistribute — just credit the original author.

---

##  Author

**Marcel Assie**
GeoAI & Geomatics Engineer in training @ ENSG
Passionate about maps, intelligent systems, and building useful & creative tools.

[LinkedIn](https://www.linkedin.com/in/marcel-assie/)
Suggestions, ideas, or bugs? [Open an issue](https://github.com/MarcelAssie/GeoGuessAI.git/issues)

---

> “Let’s make spatial intelligence playful, accessible, and powerful.”

