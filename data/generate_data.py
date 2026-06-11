"""
generate_data.py
----------------
Genera un dataset sintético de rotación laboral (employee attrition).
Simula patrones realistas entre variables HR y la probabilidad de abandono.
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
np.random.seed(SEED)

N = 1500
DEPARTMENTS = ["Ventas", "Tecnología", "RR.HH.", "Finanzas", "Operaciones", "Marketing"]
DEPT_WEIGHTS = [0.25, 0.22, 0.12, 0.15, 0.16, 0.10]


def generate_dataset(n: int = N, save: bool = True) -> pd.DataFrame:
    """
    Genera el dataset de attrition y opcionalmente lo guarda en data/employees.csv.
    Las señales son más pronunciadas para un modelo más predictivo.
    """
    edad             = np.random.randint(22, 60, n)
    anos_empresa     = np.clip(np.random.exponential(5, n).astype(int), 0, 35)
    salario          = np.random.normal(55_000, 18_000, n).clip(22_000, 130_000).astype(int)
    satisfaccion     = np.random.choice([1, 2, 3, 4, 5], n, p=[0.10, 0.18, 0.32, 0.25, 0.15])
    horas_trabajadas = np.random.normal(45, 9, n).clip(30, 80).astype(int)
    promociones      = np.random.poisson(0.8, n).clip(0, 5)
    departamento     = np.random.choice(DEPARTMENTS, n, p=DEPT_WEIGHTS)

    # Score de riesgo con señales más fuertes
    riesgo = (
        - 0.8  * (satisfaccion - 3)                       # satisfacción baja → alto riesgo
        + 0.04 * np.maximum(0, horas_trabajadas - 45)     # overtime penaliza
        - 0.025 * (salario / 10_000 - 5)                  # salario bajo → riesgo
        - 0.35 * promociones                              # sin promociones → riesgo
        - 0.06 * anos_empresa                             # mayor antigüedad → retención
        + 0.02 * np.maximum(0, 35 - edad)                # jóvenes → mayor movilidad
    )

    dept_risk = {
        "Ventas":      0.30,
        "Tecnología":  0.15,
        "RR.HH.":     -0.20,
        "Finanzas":    0.00,
        "Operaciones": 0.10,
        "Marketing":   0.20,
    }
    riesgo += np.array([dept_risk[d] for d in departamento])

    prob_abandono = 1 / (1 + np.exp(-riesgo))
    abandono = (np.random.uniform(0, 1, n) < prob_abandono).astype(int)

    df = pd.DataFrame({
        "edad":             edad,
        "anos_empresa":     anos_empresa,
        "salario":          salario,
        "satisfaccion":     satisfaccion,
        "horas_trabajadas": horas_trabajadas,
        "promociones":      promociones,
        "departamento":     departamento,
        "abandono":         abandono,
    })

    if save:
        out_path = Path(__file__).parent / "employees.csv"
        df.to_csv(out_path, index=False)
        print(f"[generate_data] Dataset guardado → {out_path}  ({n} filas)")

    return df


if __name__ == "__main__":
    df = generate_dataset()
    print(df.head())
    print(f"\nTasa de abandono: {df['abandono'].mean():.1%}")
