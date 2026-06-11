"""
tabs/prediccionmodelo.py
------------------------
Pestaña 4: Predicción en Tiempo Real
Formulario interactivo que carga model.pkl y realiza
predicciones individuales con indicador visual de riesgo.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html, no_update
import dash_bootstrap_components as dbc

# ── Paleta compartida ─────────────────────────────────────────────────────────
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

DEPARTMENTS = ["Ventas", "Tecnología", "RR.HH.", "Finanzas", "Operaciones", "Marketing"]

CARD_STYLE = {
    "borderRadius": "16px",
    "border": "none",
    "boxShadow": "0 2px 12px rgba(0,0,0,0.07)",
    "background": PASTEL["card"],
}

PLOT_CONFIG = {"displayModeBar": False}


def _load_model():
    """Carga el pipeline entrenado (importación lazy para no bloquear el app)."""
    from model.train_model import load_model
    return load_model()


def _risk_color(prob: float) -> tuple[str, str, str]:
    """Retorna (color_borde, color_bg, emoji) según nivel de riesgo."""
    if prob < 0.35:
        return PASTEL["green"], f"{PASTEL['green']}22", "🟢"
    elif prob < 0.60:
        return PASTEL["yellow"], f"{PASTEL['yellow']}33", "🟡"
    else:
        return PASTEL["peach"], f"{PASTEL['peach']}33", "🔴"


def _gauge_figure(prob: float) -> go.Figure:
    """Gauge de probabilidad de abandono (0–100%)."""
    color, _, _ = _risk_color(prob)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob * 100, 1),
        number=dict(suffix="%", font=dict(size=40, color=PASTEL["text"])),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=PASTEL["muted"], tickwidth=1),
            bar=dict(color=color, thickness=0.28),
            bgcolor="white",
            borderwidth=0,
            steps=[
                dict(range=[0,  35], color=f"{PASTEL['green']}44"),
                dict(range=[35, 60], color=f"{PASTEL['yellow']}44"),
                dict(range=[60, 100],color=f"{PASTEL['peach']}44"),
            ],
            threshold=dict(
                line=dict(color=PASTEL["text"], width=2),
                thickness=0.75,
                value=round(prob * 100, 1),
            ),
        ),
        title=dict(text="Probabilidad de Abandono",
                   font=dict(size=14, color=PASTEL["muted"])),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=0, l=20, r=20),
        height=250,
        font_family="Inter, sans-serif",
    )
    return fig


def _input_row(label: str, component, tooltip: str = "") -> dbc.Row:
    """Fila de formulario reutilizable: label + componente."""
    return dbc.Row([
        dbc.Col(
            html.Label(label, className="fw-semibold small mb-0",
                       style={"color": PASTEL["text"]}),
            width=12,
        ),
        dbc.Col(component, width=12, className="mt-1"),
        dbc.Col(
            html.Small(tooltip, style={"color": PASTEL["muted"]}) if tooltip else html.Div(),
            width=12,
        ),
    ], className="mb-3")


# ── Layout ────────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    """Retorna el layout de la pestaña de Predicción."""

    slider_style = {"color": PASTEL["blue"]}

    return html.Div([

        # Cabecera
        dbc.Row([
            dbc.Col([
                html.H4("🔮 Predicción en Tiempo Real",
                        className="fw-bold mb-1",
                        style={"color": PASTEL["text"]}),
                html.P("Ingresa los datos de un empleado para estimar su riesgo de abandono.",
                       className="mb-0 small",
                       style={"color": PASTEL["muted"]}),
            ])
        ], className="mb-4"),

        dbc.Row([

            # ── Panel izquierdo: Formulario ───────────────────────────────────
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("📋  Datos del Empleado",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody([

                        # Edad
                        _input_row(
                            "Edad del empleado",
                            dcc.Slider(
                                id="pred-edad", min=18, max=65, value=32, step=1,
                                marks={18: "18", 30: "30", 45: "45", 65: "65"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ),

                        # Años en la empresa
                        _input_row(
                            "Años en la empresa",
                            dcc.Slider(
                                id="pred-anos", min=0, max=35, value=3, step=1,
                                marks={0: "0", 10: "10", 20: "20", 35: "35"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ),

                        # Salario
                        _input_row(
                            "Salario anual (USD)",
                            dcc.Slider(
                                id="pred-salario", min=20000, max=130000,
                                value=55000, step=1000,
                                marks={20000: "$20k", 55000: "$55k",
                                       90000: "$90k", 130000: "$130k"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ),

                        # Satisfacción
                        _input_row(
                            "Nivel de satisfacción laboral (1–5)",
                            dcc.Slider(
                                id="pred-satisfaccion", min=1, max=5, value=3, step=1,
                                marks={1: "😞 1", 2: "😕 2", 3: "😐 3",
                                       4: "🙂 4", 5: "😊 5"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            "1 = Muy insatisfecho  ·  5 = Muy satisfecho",
                        ),

                        # Horas trabajadas
                        _input_row(
                            "Horas trabajadas por semana",
                            dcc.Slider(
                                id="pred-horas", min=30, max=80, value=45, step=1,
                                marks={30: "30h", 40: "40h", 50: "50h",
                                       60: "60h", 80: "80h"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ),

                        # Promociones
                        _input_row(
                            "Número de promociones recibidas",
                            dcc.Slider(
                                id="pred-promociones", min=0, max=5, value=1, step=1,
                                marks={i: str(i) for i in range(6)},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ),

                        # Departamento
                        _input_row(
                            "Departamento",
                            dbc.Select(
                                id="pred-departamento",
                                options=[{"label": d, "value": d} for d in DEPARTMENTS],
                                value="Ventas",
                                style={"borderRadius": "10px",
                                       "border": f"1.5px solid {PASTEL['blue']}",
                                       "fontSize": "0.9rem"},
                            ),
                        ),

                        # Botón predecir
                        dbc.Button(
                            [html.Span("🔮 ", className="me-1"), "Calcular Riesgo"],
                            id="btn-predecir",
                            n_clicks=0,
                            color="primary",
                            className="w-100 mt-2",
                            style={
                                "borderRadius": "10px",
                                "background": PASTEL["blue"],
                                "border": "none",
                                "color": PASTEL["text"],
                                "fontWeight": "600",
                                "padding": "0.65rem",
                            },
                        ),

                    ], className="px-4 pb-4"),
                ], style=CARD_STYLE),
            ], md=5, className="mb-4"),

            # ── Panel derecho: Resultado ──────────────────────────────────────
            dbc.Col([

                # Gauge de probabilidad
                dbc.Card([
                    dbc.CardBody(
                        dcc.Graph(id="gauge-riesgo",
                                  figure=_gauge_figure(0.0),
                                  config=PLOT_CONFIG),
                        className="p-2",
                    ),
                ], style=CARD_STYLE, className="mb-3"),

                # Diagnóstico textual
                html.Div(id="resultado-prediccion"),

                # Factores de riesgo detectados
                html.Div(id="factores-riesgo"),

            ], md=7, className="mb-4"),
        ]),

    ], style={"backgroundColor": PASTEL["bg"], "padding": "1.5rem"})


# ── Callbacks ─────────────────────────────────────────────────────────────────

@callback(
    Output("gauge-riesgo",          "figure"),
    Output("resultado-prediccion",  "children"),
    Output("factores-riesgo",       "children"),
    Input("btn-predecir", "n_clicks"),
    State("pred-edad",          "value"),
    State("pred-anos",          "value"),
    State("pred-salario",       "value"),
    State("pred-satisfaccion",  "value"),
    State("pred-horas",         "value"),
    State("pred-promociones",   "value"),
    State("pred-departamento",  "value"),
    prevent_initial_call=True,
)
def predecir(n_clicks, edad, anos, salario, satisfaccion,
             horas, promociones, departamento):
    """
    Carga el modelo, genera la predicción y construye los componentes
    visuales de resultado.
    """
    if not n_clicks:
        return no_update, no_update, no_update

    # ── 1. Armar input ────────────────────────────────────────────────────────
    X = pd.DataFrame([{
        "edad":             edad,
        "anos_empresa":     anos,
        "salario":          salario,
        "satisfaccion":     satisfaccion,
        "horas_trabajadas": horas,
        "promociones":      promociones,
        "departamento":     departamento,
    }])

    # ── 2. Predecir ───────────────────────────────────────────────────────────
    try:
        model  = _load_model()
        prob   = float(model.predict_proba(X)[0, 1])
        pred   = int(model.predict(X)[0])
    except Exception as e:
        error_msg = dbc.Alert(
            f"⚠️ Error cargando el modelo: {e}",
            color="danger", className="rounded-3",
        )
        return _gauge_figure(0.0), error_msg, html.Div()

    # ── 3. Color y nivel ──────────────────────────────────────────────────────
    color, bg_color, emoji = _risk_color(prob)
    nivel = "BAJO" if prob < 0.35 else ("MODERADO" if prob < 0.60 else "ALTO")
    nivel_desc = {
        "BAJO":     "El empleado muestra señales estables de retención.",
        "MODERADO": "Existen algunos factores de riesgo. Se recomienda seguimiento.",
        "ALTO":     "Riesgo significativo de abandono. Se recomienda intervención inmediata.",
    }

    # ── 4. Tarjeta de resultado ───────────────────────────────────────────────
    result_card = dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.Div(emoji, className="display-5 text-center"), width=2),
                dbc.Col([
                    html.H5(f"Nivel de Riesgo: {nivel}",
                            className="fw-bold mb-1",
                            style={"color": PASTEL["text"]}),
                    html.P(nivel_desc[nivel], className="mb-1 small",
                           style={"color": PASTEL["muted"]}),
                    html.Span(
                        f"Probabilidad estimada de abandono: {prob:.1%}",
                        className="badge",
                        style={"background": color, "color": PASTEL["text"],
                               "fontSize": "0.8rem", "padding": "0.4rem 0.8rem",
                               "borderRadius": "8px"},
                    ),
                ], width=10),
            ], align="center"),
        ], className="p-3"),
    ], style={
        **CARD_STYLE,
        "borderLeft": f"5px solid {color}",
        "background": bg_color,
        "marginBottom": "1rem",
    })

    # ── 5. Factores de riesgo detectados ─────────────────────────────────────
    factores = []
    if satisfaccion <= 2:
        factores.append(("🔴", "Satisfacción muy baja",
                         f"Nivel {satisfaccion}/5. Principal predictor de rotación voluntaria."))
    elif satisfaccion == 3:
        factores.append(("🟡", "Satisfacción media",
                         "Monitorear y aplicar encuestas de clima laboral."))

    if horas > 50:
        factores.append(("🔴", "Exceso de horas trabajadas",
                         f"{horas}h/semana supera el umbral saludable (45h). "
                         "Indicador de burnout."))

    if salario < 35000:
        factores.append(("🔴", "Salario por debajo del mercado",
                         f"${salario:,} USD podría no ser competitivo para el perfil."))

    if anos < 2:
        factores.append(("🟡", "Baja antigüedad",
                         f"Con {anos} año(s), el empleado aún está en período crítico "
                         "de adaptación."))

    if promociones == 0:
        factores.append(("🟡", "Sin promociones",
                         "La ausencia de avance profesional es un factor predictor "
                         "de rotación."))

    # Factores positivos
    if satisfaccion >= 4:
        factores.append(("🟢", "Alta satisfacción laboral",
                         f"Nivel {satisfaccion}/5. Factor de retención significativo."))
    if anos >= 5:
        factores.append(("🟢", "Alta antigüedad",
                         f"{anos} años en la empresa indica fuerte vínculo organizacional."))
    if promociones >= 2:
        factores.append(("🟢", "Trayectoria de promociones",
                         f"{promociones} ascensos refleja crecimiento y reconocimiento."))

    if not factores:
        factores_content = html.P("No se detectaron factores de riesgo destacables.",
                                  className="small", style={"color": PASTEL["muted"]})
    else:
        factores_content = html.Div([
            html.Div([
                html.Span(emoji + " ", className="me-1"),
                html.Strong(titulo + ": ",
                            style={"color": PASTEL["text"], "fontSize": "0.88rem"}),
                html.Span(desc, style={"color": PASTEL["muted"], "fontSize": "0.85rem"}),
            ], className="mb-2 pb-2",
               style={"borderBottom": f"1px solid {PASTEL['muted']}22"})
            for emoji, titulo, desc in factores
        ])

    factores_card = dbc.Card([
        dbc.CardBody([
            html.H6("📌 Factores Identificados",
                    className="fw-bold mb-3",
                    style={"color": PASTEL["text"]}),
            factores_content,
        ], className="p-3"),
    ], style=CARD_STYLE)

    return _gauge_figure(prob), result_card, factores_card
