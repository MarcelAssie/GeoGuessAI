# 🌍 GeoGuessAI – The Human vs AI Geospatial Challenge 🤖🧠

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![AI-Powered](https://img.shields.io/badge/AI-Gemini%202.5%20Pro-ff9800?logo=google)](https://deepmind.google/technologies/gemini/)
[![GeoData](https://img.shields.io/badge/Data-GeoJSON%2FCSV-lightgrey?logo=openstreetmap)](https://www.openstreetmap.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🕹️ A Python-powered game where a human competes against an AI in geolocation precision. Whether you’re guessing coordinates from addresses or the other way around, **spatial data meets AI** in a fun, intelligent, and educational challenge.

---

## 🎯 Concept

**GeoGuessAI** is a geospatial guessing game where the **player** goes head-to-head with a generative **AI (Gemini 2.5 Pro)** to test spatial reasoning and geodata knowledge.

### 🧭 Game Modes
- **Address → Coordinates**: Guess the exact GPS location of a given address.
- **Coordinates → Address**: Identify the street number, street name, and city from a given pair of coordinates.

Each round alternates between the human and the AI, with scores based on the **accuracy** of the guesses. May the best geographer win!

---

## 🛠️ Features

- 🎮 **Interactive gameplay** directly in the terminal
- 🧠 **AI-powered responses** via structured prompting to Gemini
- 📍 **Scoring based on spatial precision** using the Haversine formula
- 🗺️ **Real-world dataset** (addresses and GPS coordinates)
- 📊 **Live score tracking** for both human and AI
- 🔄 **Two gameplay modes** — freely selectable at start

---

## 📸 Preview

> _(Add screenshots or animated GIFs here when you’re ready)_

```bash
Your turn!
Guess the coordinates of: 8 Rue des Écoles, Paris

Latitude: 48.8531
Longitude: 2.3488

✅ Precision: 49.1 meters — You scored +100 points!

Current score:
👤 Player: 200 pts
🤖 AI: 150 pts
````

---

## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.10 or higher
* Required packages: see `requirements.txt`

### 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/geoguessai.git
cd geoguessai
pip install -r requirements.txt
```

> Then, create a `.env` file to store your Gemini API key:

```env
API_KEY=your_google_gemini_api_key
```

---

## 🧪 Input Dataset

The game uses a CSV file named `game_data.csv` stored in the `Data/` directory.

Expected format:

```
unique_ids;latitude;longitude;communes;voies;numeros
id_001;48.8566;2.3522;Paris;Rue de Rivoli;25
...
```

> You can generate this using any open geodata source (e.g. OpenStreetMap, BAN, IGN).

---

## 🧠 AI Prompts & Behavior

The AI (Gemini 2.5 Pro) is prompted with custom messages to simulate:

* 📌 Address prediction from GPS coordinates
* 📌 GPS prediction from a given full address

⚙️ It responds in a strict Python list format for easy parsing and validation:

```python
["city_name", "street_name", street_number]
[latitude, longitude]
```

---

## 🧱 Tech Stack

| Tool            | Purpose                |
| --------------- | ---------------------- |
| 🐍 Python       | Game logic and CLI     |
| 📍 geopy        | Distance calculation   |
| 📊 pandas       | Data handling          |
| 🌱 dotenv       | API key management     |
| 🤖 Google GenAI | AI-powered predictions |

---

## 💡 Possible Enhancements

* 🖥️ Web interface with **Streamlit** or **Flask**
* 🗺️ **Folium map rendering** for visual feedback
* 🌐 Geocoding APIs integration (e.g. Nominatim, Google Maps)
* 🧑‍🤝‍🧑 Multiplayer or AI vs AI mode
* 📈 Score persistence & leaderboard
* 🧩 Progressive difficulty levels

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Feel free to fork, improve, and use it as you like.

---

## 👨‍💻 Author

**Marcel Assie**
🎓 GeoAI & Geomatics Engineer in training – ENSG
💡 Passionate about spatial data, artificial intelligence, and innovation.

🔗 [LinkedIn](https://www.linkedin.com/in/marcel-assie/)
🚀 Project built for fun, learning, and pushing the boundaries of geospatial AI! 🌍🤖

---
