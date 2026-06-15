"""
Model loading and inference logic.

Handles loading the trained scikit-learn model from disk
and running predictions against it.
"""

import os
import joblib
import numpy as np
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────────────
MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
MODEL_PATH = os.getenv("MODEL_PATH", str(MODEL_DIR / "model.pkl"))

CLASS_NAMES = ["setosa", "versicolor", "virginica"]

# ── Global model reference ───────────────────────────────────────────────────
_model = None


def load_model():
    """Load the trained model from disk into memory."""
    global _model
    _model = joblib.load(MODEL_PATH)
    print(f"[OK] Model loaded from {MODEL_PATH}")
    print(f"     Type : {type(_model).__name__}")
    return _model


def get_model():
    """Return the currently loaded model (raises if not loaded)."""
    if _model is None:
        raise RuntimeError("Model is not loaded. Call load_model() first.")
    return _model


def predict(features: list[float]) -> dict:
    """
    Run inference on a single sample.

    Parameters
    ----------
    features : list[float]
        [sepal_length, sepal_width, petal_length, petal_width]

    Returns
    -------
    dict with keys: prediction, predicted_class, probabilities
    """
    model = get_model()
    X = np.array(features).reshape(1, -1)

    prediction = int(model.predict(X)[0])
    probabilities = model.predict_proba(X)[0]

    return {
        "prediction": prediction,
        "predicted_class": CLASS_NAMES[prediction],
        "probabilities": {
            name: round(float(prob), 4)
            for name, prob in zip(CLASS_NAMES, probabilities)
        },
    }


def predict_batch(batch: list[list[float]]) -> list[dict]:
    """
    Run inference on multiple samples at once.

    Parameters
    ----------
    batch : list[list[float]]
        Each inner list is [sepal_length, sepal_width, petal_length, petal_width]

    Returns
    -------
    list[dict]
    """
    model = get_model()
    X = np.array(batch)

    predictions = model.predict(X).astype(int)
    probabilities = model.predict_proba(X)

    results = []
    for pred, probs in zip(predictions, probabilities):
        results.append(
            {
                "prediction": int(pred),
                "predicted_class": CLASS_NAMES[int(pred)],
                "probabilities": {
                    name: round(float(p), 4)
                    for name, p in zip(CLASS_NAMES, probs)
                },
            }
        )
    return results
