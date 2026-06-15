# ── Stage 1: Build & train ───────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source & train the model
COPY . .
RUN python train_model.py

# ── Stage 2: Production image ───────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install only runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Copy trained model from builder stage
COPY --from=builder /app/model/ model/

# Expose port
EXPOSE 8000

# Run the API server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
