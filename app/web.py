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
        context={"prediction_text": None},
    )


@router.post("/predict-form")
def predict_form(
    request: Request,
    category: Annotated[float, Form()],
    sellable_online: Annotated[float, Form()],
    other_colors: Annotated[float, Form()],
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
        context={"prediction_text": f"Predicted furniture price: $ {price:,.2f}"},
    )
