<<<<<<< HEAD
# 🌸 Iris Classifier – ML Inference API

A production-ready **FastAPI** application that serves a trained **scikit-learn Random Forest** model for Iris flower classification, fully containerised with **Docker**.

---

## 📁 Project Structure

```
ml_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + endpoints
│   ├── model.py         # Model loading & inference logic
│   └── schemas.py       # Request/Response Pydantic models
├── model/
│   └── model.pkl        # Trained model artifact
├── train_model.py       # Script to (re)train the model
├── Dockerfile           # Multi-stage Docker build
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Option A – Run Locally (without Docker)

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model (creates model/model.pkl)
python train_model.py

# 4. Start the API server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# The API is now live at http://localhost:8000
# Visit http://localhost:8000/docs for the interactive Swagger UI
```

### Option B – Run with Docker

```bash
# Build the image (model is trained inside the build)
docker build -t iris-api .

# Run the container
docker run -d -p 8000:8000 --name iris-api iris-api
```

The API will be available at **http://localhost:8000** (auto-redirects to Swagger UI).

Interactive docs at **http://localhost:8000/docs** (Swagger UI).

> **Note (Windows):** If `uvicorn` is not recognized, use `python -m uvicorn` instead.

---

## 📡 API Endpoints

| Method | Path             | Description                        |
| ------ | ---------------- | ---------------------------------- |
| GET    | `/`              | Redirects to Swagger UI (`/docs`)  |
| GET    | `/health`        | Health check & model status        |
| POST   | `/predict`       | Single-sample inference            |
| POST   | `/predict/batch` | Batch inference (multiple samples) |
| GET    | `/docs`          | Interactive Swagger UI             |
| GET    | `/redoc`         | Alternative ReDoc documentation    |

---

## 🧪 Example Requests & Responses

### Health Check

**Bash / macOS / Linux:**

```bash
curl http://localhost:8000/health
```

**PowerShell (Windows):**

```powershell
Invoke-RestMethod -Uri http://localhost:8000/health | ConvertTo-Json
```

**Response:**

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "RandomForestClassifier"
}
```

### Single Prediction

**Bash / macOS / Linux:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

**PowerShell (Windows):**

```powershell
$body = '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
Invoke-RestMethod -Uri http://localhost:8000/predict -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json
```

**Response:**

```json
{
  "prediction": 0,
  "predicted_class": "setosa",
  "probabilities": {
    "setosa": 1.0,
    "versicolor": 0.0,
    "virginica": 0.0
  }
}
```

### Batch Prediction

**Bash / macOS / Linux:**

```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [
      {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
      {"sepal_length": 6.7, "sepal_width": 3.0, "petal_length": 5.2, "petal_width": 2.3}
    ]
  }'
```

**PowerShell (Windows):**

```powershell
$body = '{"instances": [{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}, {"sepal_length": 6.7, "sepal_width": 3.0, "petal_length": 5.2, "petal_width": 2.3}]}'
Invoke-RestMethod -Uri http://localhost:8000/predict/batch -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Response:**

```json
{
  "predictions": [
    {
      "prediction": 0,
      "predicted_class": "setosa",
      "probabilities": { "setosa": 1.0, "versicolor": 0.0, "virginica": 0.0 }
    },
    {
      "prediction": 2,
      "predicted_class": "virginica",
      "probabilities": { "setosa": 0.0, "versicolor": 0.04, "virginica": 0.96 }
    }
  ]
}
```

---

## 🐳 Docker Commands Reference

```bash
# Build
docker build -t iris-api .

# Run (foreground)
docker run -p 8000:8000 iris-api

# Run (detached)
docker run -d -p 8000:8000 --name iris-api iris-api

# View logs
docker logs iris-api

# Stop & remove
docker stop iris-api && docker rm iris-api
```

---

## 🛠️ Tech Stack

| Layer         | Technology                             |
| ------------- | -------------------------------------- |
| Framework     | FastAPI 0.115                          |
| ML Library    | scikit-learn 1.5                       |
| Serialization | joblib                                 |
| Server        | Uvicorn (ASGI)                         |
| Container     | Docker (multi-stage, python:3.11-slim) |
| Validation    | Pydantic v2.13                         |

---

## 📄 License

MIT
=======
# ml-model-api
Step-by-step ML model serving with FastAPI + Docker — from training to containerized deployment with REST endpoints.
>>>>>>> 9cb9d443eae1f97949ba2ec9bfb803483a213ad2
