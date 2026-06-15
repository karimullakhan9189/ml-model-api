"""
Request and Response Pydantic models for the Iris classification API.
"""

from pydantic import BaseModel, Field
from typing import List


class PredictionRequest(BaseModel):
    """Schema for a single prediction request."""

    sepal_length: float = Field(
        ...,
        gt=0,
        description="Sepal length in cm",
        json_schema_extra={"example": 5.1},
    )
    sepal_width: float = Field(
        ...,
        gt=0,
        description="Sepal width in cm",
        json_schema_extra={"example": 3.5},
    )
    petal_length: float = Field(
        ...,
        gt=0,
        description="Petal length in cm",
        json_schema_extra={"example": 1.4},
    )
    petal_width: float = Field(
        ...,
        gt=0,
        description="Petal width in cm",
        json_schema_extra={"example": 0.2},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2,
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    """Schema for a single prediction response."""

    prediction: int = Field(..., description="Predicted class index (0, 1, or 2)")
    predicted_class: str = Field(
        ..., description="Human-readable class name (setosa, versicolor, virginica)"
    )
    probabilities: dict[str, float] = Field(
        ..., description="Probability for each class"
    )


class BatchPredictionRequest(BaseModel):
    """Schema for batch prediction requests."""

    instances: List[PredictionRequest] = Field(
        ..., min_length=1, description="List of input instances"
    )


class BatchPredictionResponse(BaseModel):
    """Schema for batch prediction responses."""

    predictions: List[PredictionResponse] = Field(
        ..., description="List of prediction results"
    )


class HealthResponse(BaseModel):
    """Schema for the health check endpoint."""

    model_config = {"protected_namespaces": ()}

    status: str = Field(..., description="Service health status")
    model_loaded: bool = Field(..., description="Whether the model is loaded")
    model_type: str = Field(..., description="Type of the loaded model")
