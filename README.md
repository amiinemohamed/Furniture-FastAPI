# Furniture price prediction

The application uses one FastAPI deployment for both the HTML interface and the
prediction API. The API routes are the stable gateway for clients, while the
shared prediction service loads `app/model.pkl` and keeps the training feature
order in one place.

## Run locally

From this directory, install the project dependencies and start the app:

```powershell
uv sync
uv run fastapi dev
```

Open <http://127.0.0.1:8000/> for the form or
<http://127.0.0.1:8000/docs> for the API documentation.

## Prediction API

Send six numeric values in this order: `category`, `sellable_online`,
`other_colors`, `depth`, `height`, `width`.

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/predict `
  -ContentType "application/json" `
  -Body '{"features":[5,1,0,40,80,60]}'
```

The existing `POST /predict` JSON endpoint remains available as a compatibility
alias. `GET /api/health` provides a lightweight health check.

The bundled model is a decision tree, so nearby inputs may fall into the same
leaf and receive the same price. Retraining it to produce less stepwise
predictions requires the original training dataset.

## Deploy to FastAPI Cloud

The FastAPI CLI entrypoint is configured in `pyproject.toml` as
`app.main:app`. Authenticate with FastAPI Cloud, then deploy from this directory:

```powershell
uv run fastapi deploy
```

The model artifact and application templates/static files must be included in
the deployment. Dependencies, including scikit-learn for loading the model, are
declared in `pyproject.toml`.
