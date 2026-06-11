"""
train_model.py
--------------
Entrena un modelo de Regresión Logística para predecir rotación laboral.
Guarda el pipeline completo (preprocesamiento + modelo) en model.pkl.

Uso:
    python model/train_model.py
"""

import sys
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score, roc_curve,
    precision_score, recall_score, f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ── Rutas ─────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent.parent
DATA_PATH  = ROOT / "data" / "employees.csv"
MODEL_DIR  = Path(__file__).resolve().parent
MODEL_PATH = MODEL_DIR / "model.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"

# ── Features ──────────────────────────────────────────────────────────────────
NUMERIC_FEATURES = ["edad", "anos_empresa", "salario",
                    "satisfaccion", "horas_trabajadas", "promociones"]
CATEGORICAL_FEATURES = ["departamento"]
TARGET = "abandono"


def load_data() -> pd.DataFrame:
    """Carga el CSV generado por generate_data.py."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró {DATA_PATH}. "
            "Ejecuta primero: python data/generate_data.py"
        )
    return pd.read_csv(DATA_PATH)


def build_pipeline() -> Pipeline:
    """Construye el pipeline sklearn con preprocesamiento + LR."""

    # Transformadores por tipo de columna
    numeric_transformer = Pipeline([
        ("scaler", StandardScaler()),
    ])
    categorical_transformer = Pipeline([
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, NUMERIC_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES),
    ])

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            max_iter=1000,
            random_state=42,
            class_weight="balanced",   # manejo de desbalance
            C=0.8,
        )),
    ])
    return pipeline


def compute_metrics(model, X_test, y_test) -> dict:
    """Calcula y retorna todas las métricas de evaluación."""
    y_pred      = model.predict(X_test)
    y_prob      = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)

    metrics = {
        "accuracy":  round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall":    round(recall_score(y_test, y_pred), 4),
        "f1":        round(f1_score(y_test, y_pred), 4),
        "roc_auc":   round(roc_auc_score(y_test, y_prob), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "roc_curve": {
            "fpr": [round(x, 4) for x in fpr.tolist()],
            "tpr": [round(x, 4) for x in tpr.tolist()],
        },
    }
    return metrics


def train_and_save():
    """Pipeline completo: cargar → entrenar → evaluar → guardar."""

    print("─" * 50)
    print("  Employee Attrition — Entrenamiento del Modelo")
    print("─" * 50)

    # 1. Datos
    df = load_data()
    X  = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y  = df[TARGET]
    print(f"[train] Dataset cargado: {len(df)} filas  |  "
          f"Tasa abandono: {y.mean():.1%}")

    # 2. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"[train] Train: {len(X_train)}  |  Test: {len(X_test)}")

    # 3. Entrenar
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    print("[train] Entrenamiento completado ✓")

    # 4. Métricas
    metrics = compute_metrics(pipeline, X_test, y_test)
    print(f"[train] Accuracy : {metrics['accuracy']:.4f}")
    print(f"[train] ROC-AUC  : {metrics['roc_auc']:.4f}")
    print(f"[train] F1-Score : {metrics['f1']:.4f}")

    # 5. Guardar modelo
    joblib.dump(pipeline, MODEL_PATH)
    print(f"[train] Modelo guardado → {MODEL_PATH}")

    # 6. Guardar métricas en JSON (para el dashboard)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[train] Métricas guardadas → {METRICS_PATH}")
    print("─" * 50)


def load_model():
    """
    Carga el pipeline entrenado desde model.pkl.
    Lanza FileNotFoundError si el modelo no existe.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo no encontrado en {MODEL_PATH}. "
            "Ejecuta primero: python model/train_model.py"
        )
    return joblib.load(MODEL_PATH)


if __name__ == "__main__":
    train_and_save()
