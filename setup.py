"""
setup.py
--------
Script de inicialización del proyecto.
Ejecuta en orden:
  1. Generación del dataset sintético
  2. Entrenamiento y guardado del modelo

Uso:
    python setup.py
"""

import sys
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

def main():
    print("=" * 55)
    print("  Employee Attrition — Setup Inicial")
    print("=" * 55)

    # Paso 1: Generar datos
    print("\n[1/2] Generando dataset sintético...")
    from data.generate_data import generate_dataset
    df = generate_dataset(save=True)
    print(f"      ✓ {len(df)} registros creados  |  "
          f"Tasa abandono: {df['abandono'].mean():.1%}")

    # Paso 2: Entrenar modelo
    print("\n[2/2] Entrenando modelo de Regresión Logística...")
    from model.train_model import train_and_save
    train_and_save()

    print("\n" + "=" * 55)
    print("  ✅ Setup completado exitosamente")
    print("  Ahora ejecuta:  python app.py")
    print("  Abre en:        http://localhost:8050")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
