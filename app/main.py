"""
FastAPI application – Iris Classifier Inference API.

Endpoints
---------
GET  /health        → Health check & model status
POST /predict       → Single-sample prediction
POST /predict/batch → Batch predictions
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.model import load_model, get_model, predict, predict_batch
from app.schemas import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    HealthResponse,
)


# ── Lifespan: load model once at startup ─────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML model on startup, clean up on shutdown."""
    load_model()
    yield
    # Cleanup (if needed) goes here


# ── App instance ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="Iris Classifier API",
    description=(
        "A production-ready REST API that wraps a trained scikit-learn "
        "Random Forest classifier for the classic Iris dataset. "
        "Containerised with Docker for easy deployment."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to Swagger UI docs."""
    return RedirectResponse(url="/docs")


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Return the health status of the service and whether the model is loaded."""
    try:
        model = get_model()
        return HealthResponse(
            status="healthy",
            model_loaded=True,
            model_type=type(model).__name__,
        )
    except RuntimeError:
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            model_type="N/A",
        )


@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
async def predict_single(request: PredictionRequest):
    """
    Predict the Iris species for a **single** flower sample.

    Provide sepal/petal measurements in centimetres and receive the
    predicted class along with per-class probabilities.
    """
    try:
        features = [
            request.sepal_length,
            request.sepal_width,
            request.petal_length,
            request.petal_width,
        ]
        result = predict(features)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/predict/batch", response_model=BatchPredictionResponse, tags=["Inference"]
)
async def predict_batch_endpoint(request: BatchPredictionRequest):
    """
    Predict Iris species for a **batch** of flower samples in one request.
    """
    try:
        batch = [
            [
                inst.sepal_length,
                inst.sepal_width,
                inst.petal_length,
                inst.petal_width,
            ]
            for inst in request.instances
        ]
        results = predict_batch(batch)
        return BatchPredictionResponse(
            predictions=[PredictionResponse(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
