"""
Train a simple Random Forest classifier on the Iris dataset
and persist it to model/model.pkl.

Run once before starting the API:
    python train_model.py
"""

import joblib
from pathlib import Path
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ── Paths ────────────────────────────────────────────────────────────────────
MODEL_DIR = Path(__file__).resolve().parent / "model"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "model.pkl"

# ── Data ─────────────────────────────────────────────────────────────────────
print("[*] Loading Iris dataset ...")
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# ── Train ────────────────────────────────────────────────────────────────────
print("[*] Training Random Forest classifier ...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# ── Evaluate ─────────────────────────────────────────────────────────────────
y_pred = clf.predict(X_test)
print("\n[*] Classification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# ── Save ─────────────────────────────────────────────────────────────────────
joblib.dump(clf, MODEL_PATH)
print(f"\n[OK] Model saved to {MODEL_PATH}")
