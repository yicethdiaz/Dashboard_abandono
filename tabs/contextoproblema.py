"""
tabs/contextoproblema.py
------------------------
Pestaña 1: Contexto del Problema
Presenta el impacto empresarial de la rotación laboral con KPIs,
tarjetas informativas y justificación del análisis.
"""

import dash_bootstrap_components as dbc
from dash import html

# ── Paleta de colores pasteles compartida ─────────────────────────────────────
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


def _kpi_card(value: str, label: str, icon: str, color: str) -> dbc.Col:
    """Genera una tarjeta KPI reutilizable."""
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Div(icon, className="fs-2 mb-2"),
                html.H2(value, className="fw-bold mb-1",
                        style={"color": PASTEL["text"], "fontSize": "2rem"}),
                html.P(label, className="mb-0 small",
                       style={"color": PASTEL["muted"]}),
            ], className="text-center py-4"),
        ], style={
            "borderRadius": "16px",
            "border": "none",
            "boxShadow": "0 2px 12px rgba(0,0,0,0.07)",
            "borderTop": f"4px solid {color}",
            "background": PASTEL["card"],
        }),
        xs=12, sm=6, lg=3, className="mb-4",
    )


def _impact_card(title: str, body: str, color: str, icon: str) -> dbc.Col:
    """Genera una tarjeta de impacto con ícono y borde lateral."""
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.Span(icon, className="me-2 fs-5"),
                    html.Span(title, className="fw-semibold",
                              style={"color": PASTEL["text"], "fontSize": "1rem"}),
                ], className="mb-2"),
                html.P(body, className="mb-0 small",
                       style={"color": PASTEL["muted"], "lineHeight": "1.6"}),
            ], className="py-3 px-4"),
        ], style={
            "borderRadius": "12px",
            "border": "none",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.06)",
            "borderLeft": f"5px solid {color}",
            "background": PASTEL["card"],
        }),
        xs=12, md=6, className="mb-3",
    )


def layout() -> html.Div:
    """
    Retorna el layout completo de la pestaña 'Contexto del Problema'.
    Completamente autocontenida, sin dependencias externas de callbacks.
    """
    return html.Div([

        # ── Hero section ──────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Span("🏢", className="display-4 me-3"),
                    html.Div([
                        html.H1("Rotación Laboral en las Organizaciones",
                                className="fw-bold mb-1",
                                style={"color": PASTEL["text"], "fontSize": "1.9rem"}),
                        html.P(
                            "El costo oculto que transforma la estrategia de talento humano",
                            className="mb-0",
                            style={"color": PASTEL["muted"], "fontSize": "1.05rem"},
                        ),
                    ]),
                ], className="d-flex align-items-center"),
            ])
        ], className="mb-4 pt-2"),

        # ── KPIs globales ─────────────────────────────────────────────────────
        dbc.Row([
            _kpi_card("~18%",  "Tasa media de rotación anual global",  "📊", PASTEL["blue"]),
            _kpi_card("2x",    "Costo de reemplazo vs. salario anual", "💸", PASTEL["peach"]),
            _kpi_card("~42d",  "Tiempo promedio para cubrir una vacante", "⏱️", PASTEL["purple"]),
            _kpi_card("33%",   "Empleados activamente en búsqueda",    "🔍", PASTEL["green"]),
        ]),

        # ── Definición del problema ───────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("¿Qué es la Rotación Laboral?",
                                className="fw-bold mb-3",
                                style={"color": PASTEL["text"]}),
                        html.P([
                            "La ", html.Strong("rotación laboral (employee attrition)"),
                            """ es el proceso por el cual los colaboradores abandonan una 
                            organización voluntaria o involuntariamente. Más allá de ser 
                            un indicador de RRHH, representa un """,
                            html.Strong("riesgo operativo, financiero y cultural"),
                            """ que impacta la productividad, el conocimiento institucional 
                            y la moral del equipo.""",
                        ], style={"color": PASTEL["muted"], "lineHeight": "1.8"}),
                        html.P([
                            """Los modelos predictivos permiten identificar empleados en 
                            riesgo """, html.Em("antes"), """ de que decidan irse, 
                            habilitando intervenciones proactivas y focalizadas que 
                            reducen significativamente el costo de rotación.""",
                        ], className="mb-0",
                           style={"color": PASTEL["muted"], "lineHeight": "1.8"}),
                    ], className="p-4"),
                ], style={
                    "borderRadius": "16px", "border": "none",
                    "boxShadow": "0 2px 12px rgba(0,0,0,0.07)",
                    "borderTop": f"4px solid {PASTEL['blue']}",
                }),
            ], lg=7, className="mb-4"),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Tipos de Rotación",
                                className="fw-bold mb-3",
                                style={"color": PASTEL["text"]}),
                        *[
                            html.Div([
                                html.Span(icon, className="me-2"),
                                html.Strong(t + ": ", style={"color": PASTEL["text"]}),
                                html.Span(desc, style={"color": PASTEL["muted"],
                                                       "fontSize": "0.9rem"}),
                            ], className="mb-3")
                            for icon, t, desc in [
                                ("🚪", "Voluntaria",
                                 "El empleado decide irse. Más costosa y prevenible."),
                                ("📋", "Involuntaria",
                                 "La empresa termina el contrato. Planificable."),
                                ("🔄", "Funcional",
                                 "Salida de empleados con bajo rendimiento."),
                                ("⚠️", "Disfuncional",
                                 "Pérdida de talento clave. Alto impacto estratégico."),
                            ]
                        ],
                    ], className="p-4"),
                ], style={
                    "borderRadius": "16px", "border": "none",
                    "boxShadow": "0 2px 12px rgba(0,0,0,0.07)",
                    "borderTop": f"4px solid {PASTEL['purple']}",
                }),
            ], lg=5, className="mb-4"),
        ]),

        # ── Impactos empresariales ─────────────────────────────────────────────
        html.H5("Impactos Críticos para el Negocio",
                className="fw-bold mb-3 mt-2",
                style={"color": PASTEL["text"]}),
        dbc.Row([
            _impact_card(
                "Costo Financiero Directo",
                "Reclutar, seleccionar y capacitar un reemplazo puede costar entre "
                "50% y 200% del salario anual del puesto, dependiendo del nivel de especialización.",
                PASTEL["peach"], "💰",
            ),
            _impact_card(
                "Pérdida de Conocimiento",
                "Cada empleado que sale se lleva años de experiencia, relaciones con clientes "
                "y conocimiento de procesos que no se documenta ni transfiere fácilmente.",
                PASTEL["purple"], "🧠",
            ),
            _impact_card(
                "Impacto en Productividad",
                "Durante el período de vacante y onboarding del nuevo empleado, "
                "la productividad del equipo puede caer hasta un 25-30% de manera temporal.",
                PASTEL["blue"], "📉",
            ),
            _impact_card(
                "Moral del Equipo",
                "La salida frecuente de compañeros genera incertidumbre, sobrecarga "
                "de trabajo y desconfianza en el liderazgo, propagando el efecto de rotación.",
                PASTEL["green"], "🤝",
            ),
            _impact_card(
                "Marca Empleadora",
                "Altas tasas de rotación dañan la reputación en plataformas de empleo "
                "y dificultan atraer talento calificado en el mercado laboral.",
                PASTEL["pink"], "⭐",
            ),
            _impact_card(
                "Continuidad del Negocio",
                "En roles críticos, la salida de personal clave puede interrumpir proyectos "
                "estratégicos, afectar relaciones con clientes y retrasar entregables.",
                PASTEL["yellow"], "🔧",
            ),
        ]),

        # ── Objetivo del proyecto ─────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.Div("🎯", className="display-4 text-center"), width=2),
                            dbc.Col([
                                html.H4("Objetivo de este Dashboard",
                                        className="fw-bold mb-2",
                                        style={"color": PASTEL["text"]}),
                                html.P(
                                    """Desarrollar un sistema analítico predictivo que permita 
                                    a los equipos de RRHH identificar empleados en riesgo de 
                                    abandono, entender los factores que lo impulsan y tomar 
                                    decisiones de retención basadas en datos, reduciendo el 
                                    impacto financiero y operativo de la rotación no deseada.""",
                                    className="mb-0",
                                    style={"color": PASTEL["muted"], "lineHeight": "1.8"},
                                ),
                            ], width=10),
                        ], align="center"),
                    ], className="p-4"),
                ], style={
                    "borderRadius": "16px", "border": "none",
                    "boxShadow": "0 2px 12px rgba(0,0,0,0.07)",
                    "background": f"linear-gradient(135deg, {PASTEL['blue']}22, {PASTEL['purple']}22)",
                    "borderTop": f"4px solid {PASTEL['blue']}",
                }),
            ]),
        ], className="mb-2"),

    ], style={"backgroundColor": PASTEL["bg"], "padding": "1.5rem"})
