import json
from pathlib import Path

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_URL = "http://127.0.0.1:8000/predict"
FIELDS = ['category', 'sellable_online', 'other_colors', 'depth', 'height', 'width']

# Dictionnaire de correspondance (texte -> code) généré par train_model.py
MAPPING_FILE = Path(__file__).resolve().parent / "mapping.json"
MAPPING = json.loads(MAPPING_FILE.read_text(encoding="utf-8")) if MAPPING_FILE.exists() else {}


@app.route("/")
def index():
    return render_template("index.html", mapping=MAPPING)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        features = [float(request.form[name]) for name in FIELDS]
        response = requests.post(API_URL, json={"features": features}, timeout=10)
        response.raise_for_status()
        price = response.json()["price"]
        text = f"Furniture prediction price is: $ {price}"
    except requests.exceptions.RequestException:
        text = "Erreur : l'API de prédiction est injoignable (lancez api.py)."
    except (KeyError, ValueError):
        text = "Erreur : veuillez remplir correctement tous les champs."

    return render_template("index.html", mapping=MAPPING, prediction_text=text,
                           values=request.form)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
