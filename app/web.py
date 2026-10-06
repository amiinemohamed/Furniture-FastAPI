from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from app.prediction import predict_price

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prediction_text": None,
            "values": {
                "category": "0",
                "sellable_online": "1",
                "other_colors": "1",
                "depth": "",
                "height": "",
                "width": "",
            },
        },
    )


@router.post("/predict-form")
def predict_form(
    request: Request,
    category: Annotated[int, Form(ge=0, le=16)],
    sellable_online: Annotated[int, Form(ge=0, le=1)],
    other_colors: Annotated[int, Form(ge=0, le=1)],
    depth: Annotated[float, Form(gt=0)],
    height: Annotated[float, Form(gt=0)],
    width: Annotated[float, Form(gt=0)],
):
    price = predict_price(
        [category, sellable_online, other_colors, depth, height, width]
    )
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prediction_text": f"Predicted furniture price: $ {price:,.2f}",
            "values": {
                "category": str(category),
                "sellable_online": str(sellable_online),
                "other_colors": str(other_colors),
                "depth": str(depth),
                "height": str(height),
                "width": str(width),
            },
        },
    )
