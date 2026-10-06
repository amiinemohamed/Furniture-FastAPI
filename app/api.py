from pathlib import Path
from typing import List
import pickle

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"          # chemin relatif au projet (plus de chemin Windows en dur)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Ordre EXACT des colonnes utilisé à l'entraînement dans le notebook
FEATURE_NAMES = ['category', 'sellable_online', 'other_colors', 'depth', 'height', 'width']

app = FastAPI(title="Furniture price prediction API")


class FurnitureInput(BaseModel):
    features: List[float]   # [category, sellable_online, other_colors, depth, height, width]


@app.get("/")
def home():
    return {"message": "ML model for furniture price prediction",
            "expected_features": FEATURE_NAMES}


@app.post("/predict")
def predict(data: FurnitureInput):
    if len(data.features) != len(FEATURE_NAMES):
        raise HTTPException(
            status_code=422,
            detail=f"{len(FEATURE_NAMES)} features attendues : {FEATURE_NAMES}",
        )
    price = model.predict([data.features])[0]
    return {"price": round(float(price), 2)}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
