from functools import lru_cache
from pathlib import Path
import pickle

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

FEATURE_NAMES = (
    "category",
    "sellable_online",
    "other_colors",
    "depth",
    "height",
    "width",
)


@lru_cache(maxsize=1)
def load_model():
    with MODEL_PATH.open("rb") as model_file:
        return pickle.load(model_file)


def predict_price(features: list[float]) -> float:
    if len(features) != len(FEATURE_NAMES):
        raise ValueError(f"Expected {len(FEATURE_NAMES)} features in order: {FEATURE_NAMES}")

    prediction = load_model().predict([features])[0]
    return round(float(prediction), 2)
