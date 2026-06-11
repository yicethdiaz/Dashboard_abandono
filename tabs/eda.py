"""
tabs/eda.py
-----------
Pestaña 2: Análisis Exploratorio de Datos (EDA)
Incluye: donut de abandono, barplot departamental,
histogramas de variables continuas y mapa de correlación.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc
from pathlib import Path

# ── Paleta compartida ─────────────────────────────────────────────────────────
PASTEL = {
    "blue":    "#A8C8E8",
    "green":   "#A8D8B9",
    "peach":   "#F4C2A1",
    "purple":  "#C3B1E1",
    "yellow":  "#FAE3A0",
    "pink":    "#F2B8C6",
    "seq":     ["#C3B1E1", "#A8C8E8", "#A8D8B9", "#FAE3A0", "#F4C2A1", "#F2B8C6"],
    "bg":      "#F7F9FC",
    "card":    "#FFFFFF",
    "text":    "#2D3748",
    "muted":   "#718096",
    "abandon": "#F4C2A1",
    "retain":  "#A8D8B9",
}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "employees.csv"

CARD_STYLE = {
    "borderRadius": "16px",
    "border": "none",
    "boxShadow": "0 2px 12px rgba(0,0,0,0.07)",
    "background": PASTEL["card"],
}

PLOT_CONFIG = {"displayModeBar": False}
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="Inter, sans-serif",
    font_color=PASTEL["text"],
    margin=dict(t=40, b=20, l=20, r=20),
)


def _load_data() -> pd.DataFrame:
    """Carga el dataset de empleados."""
    return pd.read_csv(DATA_PATH)


# ── Figuras ───────────────────────────────────────────────────────────────────

def fig_donut(df: pd.DataFrame) -> go.Figure:
    """Dona con distribución de abandono."""
    counts   = df["abandono"].value_counts().sort_index()
    labels   = ["Se quedó", "Abandonó"]
    colors   = [PASTEL["retain"], PASTEL["abandon"]]
    total    = len(df)
    pct_quit = counts.get(1, 0) / total * 100

    fig = go.Figure(go.Pie(
        labels=labels,
        values=[counts.get(0, 0), counts.get(1, 0)],
        hole=0.62,
        marker_colors=colors,
        textinfo="percent",
        textfont_size=13,
        hovertemplate="<b>%{label}</b><br>%{value} empleados<br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(
        text=f"<b>{pct_quit:.1f}%</b><br><span style='font-size:11px'>abandono</span>",
        x=0.5, y=0.5, font_size=20, showarrow=False,
        font=dict(color=PASTEL["text"]),
    )
    fig.update_layout(
        **PLOT_LAYOUT,
        showlegend=True,
        legend=dict(orientation="h", y=-0.05, x=0.15),
        height=300,
    )
    return fig


def fig_dept_bar(df: pd.DataFrame) -> go.Figure:
    """Barras apiladas de abandono por departamento."""
    grp = (
        df.groupby(["departamento", "abandono"])
          .size()
          .reset_index(name="count")
    )
    grp["label"] = grp["abandono"].map({0: "Se quedó", 1: "Abandonó"})

    fig = px.bar(
        grp, x="departamento", y="count", color="label",
        color_discrete_map={"Se quedó": PASTEL["retain"], "Abandonó": PASTEL["abandon"]},
        barmode="stack",
        labels={"count": "Empleados", "departamento": "", "label": ""},
    )
    fig.update_layout(
        **PLOT_LAYOUT,
        height=320,
        legend=dict(orientation="h", y=1.08, x=0),
        xaxis=dict(tickfont_size=11),
    )
    fig.update_traces(marker_line_width=0)
    return fig


def fig_histograms(df: pd.DataFrame) -> go.Figure:
    """Grid 2×2 de histogramas para variables continuas."""
    variables = [
        ("edad",             "Edad",               PASTEL["blue"]),
        ("salario",          "Salario (USD)",       PASTEL["purple"]),
        ("anos_empresa",     "Años en empresa",     PASTEL["green"]),
        ("horas_trabajadas", "Horas trabajadas/sem",PASTEL["peach"]),
    ]
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=2, cols=2, subplot_titles=[v[1] for v in variables])

    for idx, (col, title, color) in enumerate(variables):
        row, c = divmod(idx, 2)
        fig.add_trace(
            go.Histogram(
                x=df[col], nbinsx=24,
                marker_color=color,
                marker_line_color="white",
                marker_line_width=0.5,
                name=title,
                hovertemplate=f"<b>{title}</b><br>Rango: %{{x}}<br>Empleados: %{{y}}<extra></extra>",
            ),
            row=row + 1, col=c + 1,
        )

    fig.update_layout(
        **PLOT_LAYOUT,
        height=420,
        showlegend=False,
    )
    fig.update_annotations(font_size=12)
    return fig


def fig_correlation(df: pd.DataFrame) -> go.Figure:
    """Mapa de calor de correlaciones numéricas."""
    num_cols = ["edad", "anos_empresa", "salario",
                "satisfaccion", "horas_trabajadas", "promociones", "abandono"]
    labels_map = {
        "edad": "Edad",
        "anos_empresa": "Años empresa",
        "salario": "Salario",
        "satisfaccion": "Satisfacción",
        "horas_trabajadas": "Horas trab.",
        "promociones": "Promociones",
        "abandono": "Abandono",
    }
    corr = df[num_cols].corr().round(2)
    labels = [labels_map[c] for c in num_cols]

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=labels,
        y=labels,
        colorscale=[
            [0.0,  "#A8C8E8"],
            [0.5,  "#FFFFFF"],
            [1.0,  "#F4C2A1"],
        ],
        zmid=0,
        text=corr.values,
        texttemplate="%{text}",
        textfont_size=10,
        hovertemplate="<b>%{x}</b> × <b>%{y}</b><br>r = %{z}<extra></extra>",
    ))
    fig.update_layout(
        **PLOT_LAYOUT,
        height=380,
        xaxis=dict(tickfont_size=10),
        yaxis=dict(tickfont_size=10, autorange="reversed"),
    )
    return fig


def fig_satisfaccion_box(df: pd.DataFrame) -> go.Figure:
    """Violín de satisfacción segmentado por abandono."""
    df2 = df.copy()
    df2["Estado"] = df2["abandono"].map({0: "Se quedó", 1: "Abandonó"})

    fig = px.violin(
        df2, x="Estado", y="satisfaccion", color="Estado",
        color_discrete_map={"Se quedó": PASTEL["retain"], "Abandonó": PASTEL["abandon"]},
        box=True, points="outliers",
        labels={"satisfaccion": "Nivel de Satisfacción", "Estado": ""},
    )
    fig.update_layout(
        **PLOT_LAYOUT,
        height=320,
        showlegend=False,
    )
    return fig


# ── Layout ────────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    """Retorna el layout completo de la pestaña EDA."""

    df = _load_data()

    # Métricas rápidas
    n_total   = len(df)
    n_quit    = df["abandono"].sum()
    avg_sal   = df["salario"].mean()
    avg_years = df["anos_empresa"].mean()

    return html.Div([

        # Cabecera
        dbc.Row([
            dbc.Col([
                html.H4("📊 Análisis Exploratorio de Datos",
                        className="fw-bold mb-1",
                        style={"color": PASTEL["text"]}),
                html.P(f"Dataset: {n_total} empleados  ·  "
                       f"{n_quit} abandonos ({n_quit/n_total:.1%})  ·  "
                       f"Salario medio: ${avg_sal:,.0f}  ·  "
                       f"Antigüedad media: {avg_years:.1f} años",
                       className="mb-0 small",
                       style={"color": PASTEL["muted"]}),
            ])
        ], className="mb-4"),

        # ── Fila 1: Donut + Barras departamento ──────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("🍩  Distribución de Abandono",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig_donut(df), config=PLOT_CONFIG),
                        className="pt-0",
                    ),
                ], style=CARD_STYLE),
            ], md=5, className="mb-4"),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("🏢  Abandono por Departamento",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig_dept_bar(df), config=PLOT_CONFIG),
                        className="pt-0",
                    ),
                ], style=CARD_STYLE),
            ], md=7, className="mb-4"),
        ]),

        # ── Fila 2: Histogramas ───────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("📈  Distribución de Variables Continuas",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig_histograms(df), config=PLOT_CONFIG),
                        className="pt-0",
                    ),
                ], style=CARD_STYLE),
            ], md=8, className="mb-4"),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("🎻  Satisfacción vs. Abandono",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig_satisfaccion_box(df), config=PLOT_CONFIG),
                        className="pt-0",
                    ),
                ], style=CARD_STYLE),
            ], md=4, className="mb-4"),
        ]),

        # ── Fila 3: Correlación ───────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Span("🔗  Matriz de Correlación",
                                  className="fw-semibold small",
                                  style={"color": PASTEL["text"]}),
                        style={"background": "transparent", "borderBottom": "none"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig_correlation(df), config=PLOT_CONFIG),
                        className="pt-0",
                    ),
                ], style=CARD_STYLE),
            ], className="mb-4"),
        ]),

    ], style={"backgroundColor": PASTEL["bg"], "padding": "1.5rem"})
