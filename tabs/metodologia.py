"""
tabs/metodologia.py
-------------------
Pestaña: Metodología
Describe el dataset sintético, el preprocesamiento,
el modelo de Regresión Logística y el pipeline completo.
"""

import dash_bootstrap_components as dbc
from dash import html

PASTEL = {
    "blue":   "#A8C8E8",
    "green":  "#A8D8B9",
    "peach":  "#F4C2A1",
    "purple": "#C3B1E1",
    "yellow": "#FAE3A0",
    "pink":   "#F2B8C6",
    "bg":     "#F7F9FC",
    "card":   "#FFFFFF",
    "text":   "#2D3748",
    "muted":  "#718096",
}

CARD_STYLE = {
    "borderRadius": "16px",
    "border": "none",
    "boxShadow": "0 2px 12px rgba(0,0,0,0.07)",
    "background": PASTEL["card"],
}

VARIABLES = [
    ("edad",             "int",   "Edad del empleado",                     "22–60",   PASTEL["blue"]),
    ("anos_empresa",     "int",   "Años trabajados en la empresa",          "0–35",    PASTEL["green"]),
    ("salario",          "int",   "Salario anual en USD",                   "22k–130k",PASTEL["peach"]),
    ("satisfaccion",     "int",   "Nivel de satisfacción laboral (escala)", "1–5",     PASTEL["purple"]),
    ("horas_trabajadas", "int",   "Horas trabajadas por semana",            "30–80",   PASTEL["yellow"]),
    ("promociones",      "int",   "Número de promociones recibidas",        "0–5",     PASTEL["pink"]),
    ("departamento",     "str",   "Departamento al que pertenece",          "6 cats",  PASTEL["blue"]),
    ("abandono",         "bool",  "Variable objetivo (1 = abandonó)",       "0/1",     PASTEL["peach"]),
]

PIPELINE_STEPS = [
    ("1", "Generación de datos",  "generate_data.py genera 1.500 registros sintéticos "
                                  "con patrones realistas entre variables HR y abandono.",
     PASTEL["blue"]),
    ("2", "División Train/Test",  "80% entrenamiento · 20% prueba. "
                                  "Estratificado por la clase objetivo para mantener proporciones.",
     PASTEL["green"]),
    ("3", "Preprocesamiento",     "StandardScaler en variables numéricas · "
                                  "OneHotEncoder para departamento. "
                                  "Implementado con ColumnTransformer en el pipeline sklearn.",
     PASTEL["purple"]),
    ("4", "Entrenamiento",        "LogisticRegression(C=0.8, class_weight='balanced', max_iter=1000). "
                                  "El parámetro class_weight corrige el desbalance de clases.",
     PASTEL["peach"]),
    ("5", "Evaluación",           "Accuracy, Precision, Recall, F1-Score, ROC-AUC, "
                                  "Curva ROC y Matriz de Confusión calculados sobre el test set.",
     PASTEL["yellow"]),
    ("6", "Persistencia",         "Pipeline completo serializado con joblib.dump() en model.pkl. "
                                  "Métricas guardadas en metrics.json para el dashboard.",
     PASTEL["pink"]),
]


def layout() -> html.Div:
    """Retorna el layout de la pestaña Metodología."""
    return html.Div([

        # Cabecera
        dbc.Row([
            dbc.Col([
                html.H4("⚙️ Metodología",
                        className="fw-bold mb-1",
                        style={"color": PASTEL["text"]}),
                html.P("Dataset sintético · Pipeline sklearn · Regresión Logística",
                       className="mb-0 small",
                       style={"color": PASTEL["muted"]}),
            ])
        ], className="mb-4"),

        # ── Dataset ──────────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📂 Dataset Sintético de Empleados",
                                className="fw-bold mb-1",
                                style={"color": PASTEL["text"]}),
                        html.P(
                            "Generado mediante generate_data.py usando NumPy con seed fija "
                            "para reproducibilidad. El score de riesgo se construye como "
                            "combinación lineal ponderada de features, transformado con "
                            "una función logística para obtener probabilidades realistas de abandono.",
                            className="mb-3 small",
                            style={"color": PASTEL["muted"], "lineHeight": "1.7"},
                        ),
                        # Tabla de variables
                        html.Div([
                            # Encabezados
                            dbc.Row([
                                dbc.Col(html.Span("Variable", className="fw-semibold small",
                                                  style={"color": PASTEL["muted"]}), width=3),
                                dbc.Col(html.Span("Tipo", className="fw-semibold small",
                                                  style={"color": PASTEL["muted"]}), width=1),
                                dbc.Col(html.Span("Descripción", className="fw-semibold small",
                                                  style={"color": PASTEL["muted"]}), width=5),
                                dbc.Col(html.Span("Rango", className="fw-semibold small",
                                                  style={"color": PASTEL["muted"]}), width=3),
                            ], className="mb-2 pb-1",
                               style={"borderBottom": f"2px solid {PASTEL['muted']}33"}),
                            # Filas
                            *[
                                dbc.Row([
                                    dbc.Col(
                                        html.Code(var, style={
                                            "background": f"{color}33",
                                            "padding": "2px 7px",
                                            "borderRadius": "5px",
                                            "fontSize": "0.82rem",
                                            "color": PASTEL["text"],
                                        }),
                                        width=3,
                                    ),
                                    dbc.Col(
                                        html.Span(tipo, className="badge",
                                                  style={
                                                      "background": f"{PASTEL['muted']}22",
                                                      "color": PASTEL["muted"],
                                                      "fontSize": "0.75rem",
                                                  }),
                                        width=1,
                                    ),
                                    dbc.Col(
                                        html.Span(desc, className="small",
                                                  style={"color": PASTEL["muted"]}),
                                        width=5,
                                    ),
                                    dbc.Col(
                                        html.Span(rango, className="small",
                                                  style={"color": PASTEL["text"],
                                                         "fontWeight": "500"}),
                                        width=3,
                                    ),
                                ], className="py-2",
                                   style={"borderBottom": f"1px solid {PASTEL['muted']}18"})
                                for var, tipo, desc, rango, color in VARIABLES
                            ],
                        ]),
                    ], className="p-4"),
                ], style=CARD_STYLE),
            ], className="mb-4"),
        ]),

        # ── Pipeline ──────────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🔄 Pipeline de Modelado",
                                className="fw-bold mb-4",
                                style={"color": PASTEL["text"]}),
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    # Número del paso
                                    html.Div(num, style={
                                        "width": "32px", "height": "32px",
                                        "borderRadius": "50%",
                                        "background": color,
                                        "color": PASTEL["text"],
                                        "fontWeight": "700",
                                        "fontSize": "0.9rem",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "flexShrink": "0",
                                    }),
                                    # Línea vertical
                                    html.Div(style={
                                        "width": "2px",
                                        "background": f"{color}55",
                                        "flexGrow": "1",
                                        "margin": "4px auto",
                                        "display": "none" if i == len(PIPELINE_STEPS) - 1 else "block",
                                    }) if False else html.Div(),
                                ], className="d-flex flex-column align-items-center me-3",
                                   style={"minWidth": "32px"}),
                                html.Div([
                                    html.Strong(titulo,
                                                style={"color": PASTEL["text"],
                                                       "fontSize": "0.92rem"}),
                                    html.P(desc, className="mb-0 small mt-1",
                                           style={"color": PASTEL["muted"],
                                                  "lineHeight": "1.6"}),
                                ], style={"paddingBottom": "1.2rem",
                                          "borderBottom": f"1px dashed {PASTEL['muted']}33"}),
                            ], className="d-flex mb-1")
                            for i, (num, titulo, desc, color) in enumerate(PIPELINE_STEPS)
                        ]),
                    ], className="p-4"),
                ], style=CARD_STYLE),
            ], md=7, className="mb-4"),

            # ── Ficha técnica del modelo ──────────────────────────────────────
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🧪 Ficha Técnica del Modelo",
                                className="fw-bold mb-3",
                                style={"color": PASTEL["text"]}),
                        *[
                            html.Div([
                                html.Span(lbl + ": ",
                                          className="fw-semibold small",
                                          style={"color": PASTEL["muted"]}),
                                html.Span(val, className="small",
                                          style={"color": PASTEL["text"]}),
                            ], className="mb-2")
                            for lbl, val in [
                                ("Algoritmo",      "Regresión Logística"),
                                ("Librería",       "scikit-learn 1.5"),
                                ("Regularización", "L2 (C=0.8)"),
                                ("Clase peso",     "balanced"),
                                ("Max iteraciones","1.000"),
                                ("Solver",         "lbfgs (default)"),
                                ("Split",          "80% train / 20% test"),
                                ("Seed",           "42 (reproducible)"),
                                ("Serialización",  "joblib.dump()"),
                            ]
                        ],
                    ], className="p-4"),
                ], style={**CARD_STYLE, "borderTop": f"4px solid {PASTEL['blue']}",
                           "marginBottom": "1rem"}),

                dbc.Card([
                    dbc.CardBody([
                        html.H6("💡 ¿Por qué Regresión Logística?",
                                className="fw-bold mb-2",
                                style={"color": PASTEL["text"]}),
                        html.P(
                            "Es el modelo de referencia (baseline) más interpretable para "
                            "clasificación binaria. Sus coeficientes tienen significado "
                            "directo: el signo y magnitud indican dirección e importancia "
                            "de cada variable en la probabilidad de abandono.",
                            className="mb-0 small",
                            style={"color": PASTEL["muted"], "lineHeight": "1.7"},
                        ),
                    ], className="p-4"),
                ], style={**CARD_STYLE, "borderTop": f"4px solid {PASTEL['green']}"}),

            ], md=5, className="mb-4"),
        ]),

    ], style={"backgroundColor": PASTEL["bg"], "padding": "1.5rem"})
