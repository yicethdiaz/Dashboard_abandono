"""
app.py
------
Punto de entrada principal del dashboard de Rotación Laboral.
Implementa navegación por pestañas; cada pestaña importa
su layout desde /tabs de forma completamente desacoplada.

Estructura:
    app.py                   ← este archivo
    data/generate_data.py    ← genera employees.csv
    model/train_model.py     ← entrena y guarda model.pkl + metrics.json
    tabs/contextoproblema.py ← pestaña 1
    tabs/metodologia.py      ← pestaña 2
    tabs/eda.py              ← pestaña 3
    tabs/metricasmodelo.py   ← pestaña 4
    tabs/prediccionmodelo.py ← pestaña 5
"""

import sys
from pathlib import Path

# ── Agregar raíz al path para imports relativos de /model y /tabs ─────────────
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

# ── Importar layouts de cada pestaña ──────────────────────────────────────────
from tabs.contextoproblema  import layout as layout_contexto
from tabs.metodologia       import layout as layout_metodologia
from tabs.eda               import layout as layout_eda
from tabs.metricasmodelo    import layout as layout_metricas
from tabs.prediccionmodelo  import layout as layout_prediccion

# ── Paleta de colores ─────────────────────────────────────────────────────────
PASTEL = {
    "blue":   "#A8C8E8",
    "green":  "#A8D8B9",
    "peach":  "#F4C2A1",
    "purple": "#C3B1E1",
    "bg":     "#F7F9FC",
    "text":   "#2D3748",
    "muted":  "#718096",
    "white":  "#FFFFFF",
    "nav_bg": "#FFFFFF",
}

# ── Inicialización de la app ──────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    ],
    suppress_callback_exceptions=True,  # necesario con callbacks en módulos externos
    title="Employee Attrition Analytics",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server  # exponer para despliegues WSGI (Gunicorn, etc.)


# ── Configuración de pestañas ─────────────────────────────────────────────────
TABS = [
    {"id": "tab-contexto",    "label": "🏢 Contexto",     "icon": ""},
    {"id": "tab-metodologia", "label": "⚙️ Metodología",  "icon": ""},
    {"id": "tab-eda",         "label": "📊 EDA",           "icon": ""},
    {"id": "tab-metricas",    "label": "🎯 Métricas",      "icon": ""},
    {"id": "tab-prediccion",  "label": "🔮 Predicción",    "icon": ""},
]


def _make_tab(tab_config: dict) -> dbc.Tab:
    """Genera un objeto dbc.Tab con estilos personalizados."""
    return dbc.Tab(
        label=tab_config["label"],
        tab_id=tab_config["id"],
        label_style={
            "fontFamily": "Inter, sans-serif",
            "fontSize": "0.88rem",
            "fontWeight": "500",
            "color": PASTEL["muted"],
            "padding": "0.65rem 1.2rem",
            "borderRadius": "10px 10px 0 0",
        },
        active_label_style={
            "fontFamily": "Inter, sans-serif",
            "fontSize": "0.88rem",
            "fontWeight": "600",
            "color": PASTEL["text"],
            "background": PASTEL["bg"],
            "borderBottom": f"3px solid {PASTEL['blue']}",
        },
    )


# ── Layout principal ──────────────────────────────────────────────────────────
app.layout = html.Div(
    style={"fontFamily": "Inter, sans-serif", "minHeight": "100vh",
           "backgroundColor": PASTEL["bg"]},
    children=[

        # ── Navbar / Header ───────────────────────────────────────────────────
        html.Div(
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Span("👥", className="me-2 fs-4"),
                            html.Div([
                                html.H1(
                                    "Employee Attrition Analytics",
                                    className="mb-0 fw-bold",
                                    style={"fontSize": "1.35rem", "color": PASTEL["text"]},
                                ),
                                html.P(
                                    "Plataforma de análisis predictivo de rotación laboral",
                                    className="mb-0",
                                    style={"fontSize": "0.82rem", "color": PASTEL["muted"]},
                                ),
                            ]),
                        ], className="d-flex align-items-center"),
                    ], md=8),
                    dbc.Col([
                        html.Div([
                            html.Span("🤖", className="me-1"),
                            html.Span("Powered by Logistic Regression · scikit-learn",
                                      style={"fontSize": "0.78rem", "color": PASTEL["muted"]}),
                        ], className="text-end d-none d-md-block"),
                    ], md=4),
                ], align="center"),
            ], fluid=True),
            style={
                "backgroundColor": PASTEL["white"],
                "padding": "1rem 1.5rem",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.07)",
                "marginBottom": "0",
                "position": "sticky",
                "top": "0",
                "zIndex": "1000",
            },
        ),

        # ── Pestañas ──────────────────────────────────────────────────────────
        dbc.Container([
            dbc.Tabs(
                id="main-tabs",
                active_tab="tab-contexto",
                children=[_make_tab(t) for t in TABS],
                style={
                    "marginTop": "1rem",
                    "borderBottom": f"2px solid {PASTEL['blue']}33",
                },
            ),
            # Contenedor dinámico de cada pestaña
            html.Div(id="tab-content", style={"marginTop": "0"}),
        ], fluid=True, style={"padding": "0 1rem"}),

    ],
)


# ── Callback principal: render de pestañas ─────────────────────────────────────
@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "active_tab"),
)
def render_tab(active_tab: str) -> html.Div:
    """
    Renderiza el layout de la pestaña activa.
    Cada función layout() es completamente autocontenida.
    """
    tab_map = {
        "tab-contexto":    layout_contexto,
        "tab-metodologia": layout_metodologia,
        "tab-eda":         layout_eda,
        "tab-metricas":    layout_metricas,
        "tab-prediccion":  layout_prediccion,
    }
    render_fn = tab_map.get(active_tab)
    if render_fn is None:
        return html.Div("Pestaña no encontrada",
                        className="text-center p-5",
                        style={"color": PASTEL["muted"]})
    return render_fn()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)
