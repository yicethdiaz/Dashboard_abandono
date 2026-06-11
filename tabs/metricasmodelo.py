"""
tabs/metricasmodelo.py
----------------------
Pestaña 3: Métricas del Modelo
Muestra accuracy, precision, recall, F1, ROC-AUC,
curva ROC y matriz de confusión.
"""

import json
from pathlib import Path

import plotly.graph_objects as go
from dash import dcc, html
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

METRICS_PATH = Path(__file__).resolve().parent.parent / "model" / "metrics.json"

CARD_STYLE = {
    "borderRadius": "16px",
    "border": "none",
    "boxShadow": "0 2px 12px rgba(0,0,0,0.07)",
    "background": PASTEL["card"],
}

PLOT_CONFIG  = {"displayModeBar": False}
PLOT_LAYOUT  = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="Inter, sans-serif",
    font_color=PASTEL["text"],
    margin=dict(t=40, b=20, l=20, r=20),
)


def _load_metrics() -> dict:
    """Carga métricas desde JSON generado por train_model.py."""
    with open(METRICS_PATH) as f:
        return json.load(f)


# ── Tarjeta métrica ───────────────────────────────────────────────────────────

def _metric_card(label: str, value: float, icon: str,
                 color: str, description: str) -> dbc.Col:
    pct = f"{value * 100:.1f}%"
    bar_width = f"{value * 100:.0f}%"

    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.Span(icon, className="me-2 fs-5"),
                    html.Span(label, className="fw-semibold small",
                              style={"color": PASTEL["muted"]}),
                ], className="mb-2"),
                html.H2(pct, className="fw-bold mb-1",
                        style={"color": PASTEL["text"], "fontSize": "2.2rem"}),
                # Mini barra de progreso
                html.Div(
                    html.Div(style={
                        "width": bar_width,
                        "height": "6px",
                        "borderRadius": "4px",
                        "background": color,
                        "transition": "width 0.6s ease",
                    }),
                    style={
                        "width": "100%",
                        "height": "6px",
                        "borderRadius": "4px",
                        "background": f"{color}33",
                        "marginBottom": "8px",
                    }
                ),
                html.P(description, className="mb-0",
                       style={"color": PASTEL["muted"], "fontSize": "0.78rem",
                              "lineHeight": "1.5"}),
            ], className="p-3"),
        ], style={
            **CARD_STYLE,
            "borderTop": f"4px solid {color}",
        }),
        xs=12, sm=6, lg=3, className="mb-4",
    )


# ── Figuras ───────────────────────────────────────────────────────────────────

def fig_roc(metrics: dict) -> go.Figure:
    """Curva ROC con área sombreada."""
    fpr = metrics["roc_curve"]["fpr"]
    tpr = metrics["roc_curve"]["tpr"]
    auc = metrics["roc_auc"]

    fig = go.Figure()

    # Área rellena bajo la curva
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        fill="tozeroy",
        fillcolor=f"{PASTEL['blue']}55",
        line=dict(color=PASTEL["blue"], width=2.5),
        name=f"ROC (AUC = {auc:.3f})",
        hovertemplate="FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>",
    ))

    # Línea de referencia aleatoria
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        line=dict(color=PASTEL["muted"], width=1.5, dash="dot"),
        name="Aleatorio (AUC = 0.5)",
        hoverinfo="skip",
    ))

    fig.update_layout(
        **PLOT_LAYOUT,
        height=350,
        xaxis=dict(title="Tasa Falsos Positivos", range=[0, 1]),
        yaxis=dict(title="Tasa Verdaderos Positivos", range=[0, 1]),
        legend=dict(x=0.45, y=0.1),
    )
    return fig


def fig_confusion(metrics: dict) -> go.Figure:
    """Matriz de confusión como heatmap anotado."""
    cm = metrics["confusion_matrix"]
    labels = ["Se quedó (0)", "Abandonó (1)"]

    # Texto combinado: valor + porcentaje
    total = sum(sum(row) for row in cm)
    text = [
        [f"{cm[i][j]}<br>({cm[i][j]/total:.1%})" for j in range(2)]
        for i in range(2)
    ]

    fig = go.Figure(go.Heatmap(
        z=cm,
        x=[f"Pred: {l}" for l in labels],
        y=[f"Real: {l}" for l in labels],
        colorscale=[[0, PASTEL["blue"] + "44"], [1, PASTEL["peach"]]],
        text=text,
        texttemplate="%{text}",
        textfont_size=13,
        showscale=False,
        hovertemplate="Real: %{y}<br>Predicho: %{x}<br>Cantidad: %{z}<extra></extra>",
    ))
    fig.update_layout(
        **PLOT_LAYOUT,
        height=320,
        xaxis=dict(tickfont_size=11),
        yaxis=dict(tickfont_size=11, autorange="reversed"),
    )
    return fig


def fig_gauge_f1(f1: float) -> go.Figure:
    """Gauge visual del F1-Score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=round(f1 * 100, 1),
        number=dict(suffix="%", font=dict(size=28, color=PASTEL["text"])),
        delta=dict(reference=70, increasing_color=PASTEL["green"],
                   decreasing_color=PASTEL["peach"]),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=PASTEL["muted"]),
            bar=dict(color=PASTEL["purple"], thickness=0.3),
            bgcolor="white",
            borderwidth=0,
            steps=[
                dict(range=[0, 50],  color=f"{PASTEL['peach']}66"),
                dict(range=[50, 75], color=f"{PASTEL['yellow']}66"),
                dict(range=[75, 100],color=f"{PASTEL['green']}66"),
            ],
            threshold=dict(
                line=dict(color=PASTEL["peach"], width=3),
                thickness=0.8, value=70,
            ),
        ),
        title=dict(text="F1-Score", font=dict(size=14, color=PASTEL["muted"])),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=10, l=10, r=10),
        height=220,
        font_family="Inter, sans-serif",
    )
    return fig


# ── Layout ────────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    """Retorna el layout de la pestaña Métricas del Modelo."""

    metrics = _load_metrics()

    return html.Div([

        # Cabecera
        dbc.Row([
            dbc.Col([
                html.H4("🎯 Métricas del Modelo",
                        className="fw-bold mb-1",
                        style={"color": PASTEL["text"]}),
                html.P("Evaluación del modelo de Regresión Logística · "
                       "Conjunto de prueba (20% de los datos)",
                       className="mb-0 small",
                       style={"color": PASTEL["muted"]}),
            ])
        ], className="mb-4"),

        # ── KPI Métricas ──────────────────────────────────────────────────────
        dbc.Row([
            _metric_card(
                "Accuracy", metrics["accuracy"],
                "✅", PASTEL["green"],
                "Proporción de predicciones correctas sobre el total.",
            ),
            _metric_card(
                "Precision", metrics["precision"],
                "🎯", PASTEL["blue"],
                "De los predichos como 'abandono', ¿cuántos realmente lo hicieron?",
            ),
            _metric_card(
                "Recall", metrics["recall"],
                "🔍", PASTEL["purple"],
                "De los que realmente abandonaron, ¿cuántos detectamos?",
            ),
            _metric_card(
                "ROC-AUC", metrics["roc_auc"],
                "📐", PASTEL["peach"],
                "Capacidad discriminativa global del modelo (0.5 = azar, 1.0 = perfecto).",
            ),
        ]),

        # ── ROC + Gauge ───────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("📈  Curva ROC",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig_roc(metrics), config=PLOT_CONFIG),
                        className="pt-0",
                    ),
                ], style=CARD_STYLE),
            ], md=8, className="mb-4"),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("🏅  F1-Score",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody([
                        dcc.Graph(figure=fig_gauge_f1(metrics["f1"]),
                                  config=PLOT_CONFIG),
                        html.P(
                            "Media armónica de Precision y Recall. "
                            "Ideal para clases desbalanceadas.",
                            className="text-center small mt-2 mb-0",
                            style={"color": PASTEL["muted"]},
                        ),
                    ], className="pt-0"),
                ], style=CARD_STYLE),
            ], md=4, className="mb-4"),
        ]),

        # ── Matriz de confusión + interpretación ──────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("🔲  Matriz de Confusión",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig_confusion(metrics), config=PLOT_CONFIG),
                        className="pt-0",
                    ),
                ], style=CARD_STYLE),
            ], md=6, className="mb-4"),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🔎 Interpretación",
                                className="fw-bold mb-3",
                                style={"color": PASTEL["text"]}),
                        *[
                            html.Div([
                                html.Div(style={
                                    "width": "12px", "height": "12px",
                                    "borderRadius": "3px",
                                    "background": color, "flexShrink": "0",
                                }),
                                html.Div([
                                    html.Strong(title + ": ",
                                                style={"color": PASTEL["text"],
                                                       "fontSize": "0.88rem"}),
                                    html.Span(desc,
                                              style={"color": PASTEL["muted"],
                                                     "fontSize": "0.85rem"}),
                                ]),
                            ], className="d-flex gap-2 align-items-start mb-3")
                            for color, title, desc in [
                                (PASTEL["green"],
                                 "Verdadero Positivo (TP)",
                                 "Empleados que abandonaron y el modelo predijo correctamente."),
                                (PASTEL["blue"],
                                 "Verdadero Negativo (TN)",
                                 "Empleados que no abandonaron y el modelo predijo correctamente."),
                                (PASTEL["peach"],
                                 "Falso Positivo (FP)",
                                 "El modelo predijo abandono pero el empleado se quedó. "
                                 "Intervención innecesaria."),
                                (PASTEL["purple"],
                                 "Falso Negativo (FN)",
                                 "El modelo NO predijo abandono pero el empleado sí se fue. "
                                 "El error más costoso."),
                            ]
                        ],
                        html.Hr(style={"borderColor": f"{PASTEL['muted']}33"}),
                        html.P(
                            "💡 En attrition, minimizar los Falsos Negativos "
                            "(FN) es prioritario: es preferible intervenir "
                            "con un falso positivo que perder talento clave "
                            "sin actuar.",
                            className="mb-0 small fst-italic",
                            style={"color": PASTEL["muted"], "lineHeight": "1.6"},
                        ),
                    ], className="p-4"),
                ], style=CARD_STYLE),
            ], md=6, className="mb-4"),
        ]),

    ], style={"backgroundColor": PASTEL["bg"], "padding": "1.5rem"})
