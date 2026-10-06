from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.prediction import FEATURE_NAMES, predict_price

router = APIRouter()


class FurnitureInput(BaseModel):
    features: Annotated[
        list[float],
        Field(
            min_length=len(FEATURE_NAMES),
            max_length=len(FEATURE_NAMES),
            description=f"Values ordered as {', '.join(FEATURE_NAMES)}.",
        ),
    ]


class FurniturePrediction(BaseModel):
    price: float


@router.post("/predict", response_model=FurniturePrediction, include_in_schema=False)
@router.post("/api/predict", response_model=FurniturePrediction)
def predict(data: FurnitureInput) -> FurniturePrediction:
    return FurniturePrediction(price=predict_price(data.features))


@router.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
