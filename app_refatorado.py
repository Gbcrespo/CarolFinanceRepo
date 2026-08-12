import math
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Planejamento Financeiro | Dra. Carolina Bittencourt",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PALETA / CONSTANTES VISUAIS
# ============================================================
BG = "#FBF9F7"
CARD = "#FFFFFF"
TEXT = "#2C3E50"
MUTED = "#6B7280"

ROSE = "#E8D5D0"
ROSE_DARK = "#B9867C"
NUDE = "#F3E9E4"
GOLD = "#C8A56A"

GREEN = "#6F9D85"
GREEN_SOFT = "#E8F2EC"

CREAM = "#FFF9F2"
BORDER = "#E8E1DC"
GRID = "#ECE7E3"

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "scrollZoom": False,
    "doubleClick": False,
    "showTips": False,
    "responsive": True,
}


# ============================================================
# CSS — TEMA CLARO E CONTRASTE CONSISTENTE
# ============================================================
st.markdown(
    f"""
    <style>
        :root {{
            color-scheme: light !important;
        }}

        html, body, .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background-color: {BG} !important;
            color: {TEXT} !important;
        }}

        .block-container {{
            max-width: 1480px;
            padding-top: 1.6rem;
            padding-bottom: 2.6rem;
        }}

        h1, h2, h3, h4, h5, h6,
        p, label, span {{
            color: {TEXT};
        }}

        /* Cabeçalho */
        .hero {{
            background: linear-gradient(135deg, #FFFFFF 0%, {NUDE} 100%);
            border: 1px solid {BORDER};
            border-radius: 20px;
            padding: 26px 30px;
            margin-bottom: 1.1rem;
            box-shadow: 0 10px 28px rgba(61, 48, 42, 0.06);
        }}

        .hero-title {{
            font-size: 2rem;
            line-height: 1.15;
            font-weight: 760;
            letter-spacing: -0.025em;
            margin-bottom: 7px;
            color: {TEXT};
        }}

        .hero-subtitle {{
            font-size: .97rem;
            margin: 0;
            color: {MUTED};
        }}

        /* Badges */
        .badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 6px 11px;
            font-size: .78rem;
            line-height: 1;
            font-weight: 680;
            border: 1px solid transparent;
        }}

        .badge-rose {{
            background: #F7EDEA;
            color: #945F57;
            border-color: #EEDBD5;
        }}

        .badge-gold {{
            background: #FBF3E5;
            color: #8A6D3E;
            border-color: #ECDAB9;
        }}

        .badge-green {{
            background: {GREEN_SOFT};
            color: #527663;
            border-color: #D6E8DC;
        }}

        .badge-neutral {{
            background: #F5F3F1;
            color: #625D59;
            border-color: #E7E2DE;
        }}

        /* KPIs */
        .kpi-card {{
            min-height: 150px;
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 7px 22px rgba(62, 50, 44, .055);
            transition: transform .18s ease, box-shadow .18s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 13px 28px rgba(62, 50, 44, .10);
        }}

        .kpi-highlight {{
            background: linear-gradient(145deg, #FFFFFF 0%, #FBF3EF 100%);
        }}

        .kpi-profit {{
            background: linear-gradient(145deg, #FFFFFF 0%, {GREEN_SOFT} 100%);
            border-color: #D9E8DF;
        }}

        .kpi-label {{
            color: #716A66;
            font-size: .76rem;
            font-weight: 750;
            letter-spacing: .055em;
            text-transform: uppercase;
            margin-bottom: 11px;
        }}

        .kpi-value {{
            color: {TEXT};
            font-size: 1.65rem;
            line-height: 1.05;
            font-weight: 780;
            margin-bottom: 11px;
        }}

        .kpi-sub {{
            color: {MUTED};
            font-size: .82rem;
            line-height: 1.38;
        }}

        .positive {{
            color: {GREEN};
            font-weight: 750;
        }}

        /* Espaçamento explícito pedido entre KPIs e badges */
        .kpi-badges {{
            margin-top: 15px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .soft-panel {{
            background: rgba(255,255,255,.86);
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 18px 20px;
            margin: 8px 0 15px 0;
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            color: {TEXT} !important;
            font-weight: 650;
            border-radius: 10px 10px 0 0;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: #8D5E56 !important;
            background: #F5ECE8 !important;
        }}

        /* ===================================================
           CONTRASTE: EXPANDER, INPUTS, SELECTS E DROPDOWNS
           =================================================== */
        [data-testid="stExpander"] {{
            background: #FFFFFF !important;
            border: 1px solid {BORDER} !important;
            border-radius: 14px !important;
            overflow: hidden;
        }}

        [data-testid="stExpander"] details,
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary *,
        [data-testid="stExpander"] details > div {{
            background-color: #FFFFFF !important;
            color: {TEXT} !important;
            -webkit-text-fill-color: {TEXT} !important;
        }}

        [data-baseweb="input"],
        [data-baseweb="textarea"],
        [data-baseweb="select"] > div {{
            background-color: #F8F9FA !important;
            color: {TEXT} !important;
            border-color: #D9DEE3 !important;
            border-radius: 10px !important;
        }}

        [data-baseweb="input"] input,
        [data-baseweb="textarea"] textarea,
        [data-baseweb="select"] span {{
            color: {TEXT} !important;
            -webkit-text-fill-color: {TEXT} !important;
            background-color: transparent !important;
        }}

        [data-testid="stNumberInput"] button {{
            background-color: #F1F3F5 !important;
            color: {TEXT} !important;
            border-color: #D9DEE3 !important;
        }}

        [data-testid="stNumberInput"] button svg,
        [data-baseweb="select"] svg {{
            fill: {TEXT} !important;
            color: {TEXT} !important;
        }}

        [data-baseweb="popover"],
        [data-baseweb="popover"] > div,
        [role="listbox"],
        [role="option"] {{
            background: #FFFFFF !important;
            color: {TEXT} !important;
        }}

        [role="option"] *,
        [role="listbox"] * {{
            color: {TEXT} !important;
            -webkit-text-fill-color: {TEXT} !important;
        }}

        [role="option"]:hover {{
            background: #F5ECE8 !important;
        }}

        [data-testid="stSlider"] p,
        [data-testid="stNumberInput"] p,
        [data-testid="stSelectbox"] p,
        [data-testid="stRadio"] p,
        [data-testid="stCheckbox"] p {{
            color: {TEXT} !important;
        }}

        /* Botões */
        .stButton > button,
        .stDownloadButton > button {{
            background: #FFFDFC !important;
            color: {TEXT} !important;
            border: 1px solid #D9CCC4 !important;
            border-radius: 10px !important;
            font-weight: 650 !important;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            color: #875A53 !important;
            background: #FAF1ED !important;
            border-color: {ROSE_DARK} !important;
        }}

        /* ===================================================
           DATA EDITOR
           =================================================== */
        .editor-tip {{
            background: #FFF7EA;
            border: 1px solid #EEDDBE;
            border-radius: 12px;
            padding: 11px 14px;
            margin: 8px 0 12px 0;
            color: #765E37;
            font-size: .86rem;
            font-weight: 620;
        }}

        .editor-status {{
            margin: 8px 0 12px 0;
        }}

        /* Oculta toolbar onde a UI permite ocultar/gerenciar colunas.
           A estrutura de colunas também é fixada pelo código Python. */
        [data-testid="stDataEditor"] [data-testid="stElementToolbar"],
        [data-testid="stDataFrame"] [data-testid="stElementToolbar"] {{
            display: none !important;
        }}

        /* ===================================================
           TABELA CALCULADA - SOMENTE LEITURA, VISUAL CREME
           =================================================== */
        .calc-table-wrap {{
            background: {CREAM};
            border: 1px solid #ECDCCD;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 6px 18px rgba(72, 60, 53, .045);
            margin: 8px 0 18px 0;
        }}

        .calc-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: .88rem;
        }}

        .calc-table thead th {{
            background: #F7EBDD;
            color: #665C54;
            text-align: left;
            padding: 12px 14px;
            font-size: .73rem;
            text-transform: uppercase;
            letter-spacing: .05em;
            font-weight: 760;
            border-bottom: 1px solid #E7D6C5;
        }}

        .calc-table tbody td {{
            padding: 11px 14px;
            color: {TEXT};
            border-bottom: 1px solid #F0E5DA;
        }}

        .calc-table tbody tr:nth-child(even) {{
            background: #FFFDF9;
        }}

        .calc-table tbody tr:last-child td {{
            border-bottom: none;
        }}

        .calc-table .product {{
            font-weight: 650;
        }}

        .calc-table .number {{
            text-align: right;
            font-variant-numeric: tabular-nums;
        }}

        .calc-table .money {{
            text-align: right;
            font-weight: 680;
            font-variant-numeric: tabular-nums;
        }}

        /* Melhor responsividade */
        @media (max-width: 900px) {{
            .hero-title {{ font-size: 1.55rem; }}
            .kpi-card {{ min-height: 125px; margin-bottom: 8px; }}
        }}

        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DADOS PADRÃO
# ============================================================
DEFAULT_INPUTS = pd.DataFrame(
    [
        ["Clorexidina 100 ml", 12.99, 1.0, "frasco", 0.10, False],
        ["Gaze", 15.48, 1.0, "caixa", 0.20, False],
        ["Seringas 50 UI", 84.00, 50.0, "unidades", 2.00, True],
        ["Seringas de 1 ml", 20.00, 50.0, "unidades", 1.00, True],
        ["Salina estéril frasquinhos", 18.25, 25.0, "unidades", 1.00, True],
        ["Luvas", 28.00, 100.0, "unidades", 2.00, False],
        ["Anestésico", 93.00, 1.0, "frasco", 0.05, False],
        ["Sabonete", 5.00, 1.0, "unidade", 0.10, False],
        ["Lápis marcador branco", 15.00, 1.0, "unidade", 0.05, False],
        ["Faixas pro cabelo", 15.00, 20.0, "unidades", 1.00, False],
    ],
    columns=[
        "Produto",
        "Preço compra (R$)",
        "Qtd total",
        "Unidade",
        "Qtd/paciente",
        "Dividido com Julia",
    ],
)

EDITOR_COLUMN_ORDER = [
    "Produto",
    "Preço compra (R$)",
    "Qtd total",
    "Unidade",
    "Qtd/paciente",
    "Dividido com Julia",
]


# ============================================================
# HELPERS
# ============================================================
def brl(value: float) -> str:
    if value is None or not np.isfinite(value):
        return "—"
    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def pct(value: float) -> str:
    if value is None or not np.isfinite(value):
        return "—"
    return f"{value * 100:.1f}%"


def round_up(value: float, step: float) -> float:
    if step <= 0:
        return value
    return math.ceil(value / step) * step


def safe_ceil_div(numerator: float, denominator: float) -> Optional[int]:
    if denominator <= 0 or not np.isfinite(denominator):
        return None
    return int(math.ceil(max(0.0, numerator) / denominator))


def kpi_card(label: str, value: str, subtitle: str, variant: str = "default") -> None:
    variant_class = ""
    if variant == "highlight":
        variant_class = "kpi-highlight"
    elif variant == "profit":
        variant_class = "kpi-profit"

    st.markdown(
        f"""
        <div class="kpi-card {variant_class}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_intro(title: str, text: str) -> None:
    st.markdown(f"### {title}")
    st.caption(text)


def push_history(df: pd.DataFrame) -> None:
    """Armazena até os 10 estados anteriores do editor."""
    history = st.session_state.setdefault("history", [])

    if history and history[-1].equals(df):
        return

    history.append(df.copy(deep=True))
    st.session_state["history"] = history[-10:]


def reset_editor_to_default() -> None:
    """Restaura padrão e permite desfazer o reset."""
    push_history(st.session_state["insumos_df"])
    st.session_state["insumos_df"] = DEFAULT_INPUTS.copy(deep=True)
    st.session_state["editor_version"] += 1
    st.session_state["editor_message"] = "Tabela restaurada para os valores padrão."


def undo_editor() -> None:
    """Restaura o último estado salvo."""
    history = st.session_state.get("history", [])
    if not history:
        return

    previous_df = history.pop()
    st.session_state["history"] = history
    st.session_state["insumos_df"] = previous_df.copy(deep=True)
    st.session_state["editor_version"] += 1
    st.session_state["editor_message"] = "Última alteração desfeita."


def style_plotly(
    fig: go.Figure,
    *,
    animated: bool = False,
    legend_orientation: Optional[str] = None,
) -> go.Figure:
    """Padroniza contraste e fundo de todos os gráficos Plotly."""
    layout_updates = dict(
        template="plotly_white",
        font_color=TEXT,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color=TEXT)),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#D8DDE2",
            font=dict(color=TEXT),
        ),
    )

    if animated:
        layout_updates.update(
            transition_duration=500,
            transition_easing="cubic-in-out",
        )

    fig.update_layout(**layout_updates)

    if legend_orientation:
        fig.update_layout(
            legend=dict(
                orientation=legend_orientation,
                font=dict(color=TEXT),
            )
        )

    fig.update_xaxes(
        color=TEXT,
        tickfont=dict(color=TEXT),
        title_font=dict(color=TEXT),
        gridcolor=GRID,
        zerolinecolor="#D9DDE1",
    )
    fig.update_yaxes(
        color=TEXT,
        tickfont=dict(color=TEXT),
        title_font=dict(color=TEXT),
        gridcolor=GRID,
        zerolinecolor="#D9DDE1",
    )
    return fig


def build_donut(cost_df: pd.DataFrame, total_realista: float) -> go.Figure:
    """
    Rosca sem texto nas fatias pequenas.
    A legenda lateral e o hover preservam todas as informações.
    """
    df = cost_df[cost_df["Custo/paciente (R$)"] > 0].copy()
    df = df.sort_values("Custo/paciente (R$)", ascending=False)

    palette = [
        GOLD,
        ROSE_DARK,
        GREEN,
        "#D9C5BC",
        "#A9BAB1",
        "#D7C8BA",
        "#C8C0BB",
        "#E5D2C9",
        "#95A99D",
        "#DDBAB3",
        "#BBA37D",
        "#CCD3CE",
        "#E5D7CA",
    ]

    fig = go.Figure(
        go.Pie(
            labels=df["Produto"],
            values=df["Custo/paciente (R$)"],
            hole=0.62,
            sort=False,
            marker=dict(
                colors=[palette[i % len(palette)] for i in range(len(df))],
                line=dict(color="#FFFFFF", width=1),
            ),
            textinfo="none",
            textposition="none",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Custo: R$ %{value:.2f}<br>"
                "Fatia: %{percent}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_annotation(
        x=0.38,
        y=0.5,
        text=f"<b>{brl(total_realista)}</b><br><span style='font-size:11px'>custo realista</span>",
        showarrow=False,
        align="center",
        font=dict(size=14, color=TEXT),
    )

    fig.update_layout(
        title=dict(
            text="Composição do custo",
            font=dict(color=TEXT, size=16),
            x=0.02,
        ),
        height=430,
        margin=dict(l=15, r=260, t=55, b=15),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(color=TEXT, size=11),
            itemsizing="constant",
            traceorder="normal",
            title=dict(text="Itens", font=dict(color=TEXT)),
        ),
    )

    style_plotly(fig)
    return fig


def build_scenario_bars(scenario_df: pd.DataFrame) -> go.Figure:
    """Barras com contraste explícito e transição de 500 ms."""
    fig = go.Figure()

    series = [
        ("Custo", "#C9C1BC"),
        ("Preço Novos", ROSE_DARK),
        ("Preço Amigos/Família", GOLD),
    ]

    for column, color in series:
        fig.add_trace(
            go.Bar(
                name=column,
                x=scenario_df["Cenário"],
                y=scenario_df[column],
                marker_color=color,
                text=scenario_df[column],
                texttemplate="R$ %{text:.2f}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    f"<b>{column}</b><br>"
                    "%{x}<br>"
                    "R$ %{y:.2f}"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title=dict(
            text="Precificação por cenário",
            font=dict(color=TEXT, size=16),
            x=0.02,
        ),
        barmode="group",
        height=430,
        margin=dict(l=15, r=15, t=85, b=35),
        yaxis_title="Valor (R$)",
        xaxis_title="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="left",
            x=0,
            font=dict(color=TEXT, size=11),
        ),
        bargap=0.25,
        uirevision="scenario-chart",
    )

    style_plotly(fig, animated=True)
    return fig


def build_break_even_chart(
    patients: np.ndarray,
    results: np.ndarray,
    be_payback: Optional[int],
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=patients,
            y=results,
            mode="lines",
            line=dict(color=ROSE_DARK, width=3),
            fill="tozeroy",
            fillcolor="rgba(185, 134, 124, 0.10)",
            hovertemplate="%{x} pacientes<br>R$ %{y:.2f}<extra></extra>",
            name="Resultado",
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="#8E969D",
        annotation_text="Equilíbrio",
        annotation_font_color=TEXT,
    )

    if be_payback is not None:
        fig.add_vline(
            x=be_payback,
            line_dash="dot",
            line_color=GOLD,
            annotation_text=f"BE: {be_payback} pac.",
            annotation_font_color=TEXT,
        )

    fig.update_layout(
        title=dict(
            text="Resultado mensal conforme o número de pacientes",
            font=dict(color=TEXT, size=16),
        ),
        height=430,
        margin=dict(l=15, r=15, t=55, b=25),
        xaxis_title="Pacientes por mês",
        yaxis_title="Resultado (R$)",
        showlegend=False,
        uirevision="breakeven-chart",
    )

    style_plotly(fig, animated=True)
    return fig


def build_flask_comparison(comparison: pd.DataFrame, dose_ui: float) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=comparison["Frasco"],
            y=comparison["Custo toxina/paciente"],
            marker_color=[ROSE_DARK, GOLD],
            text=comparison["Custo toxina/paciente"],
            texttemplate="R$ %{text:.2f}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{x}</b><br>Custo/paciente: R$ %{y:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text=f"Custo da toxina para uma aplicação de {dose_ui:.0f} UI",
            font=dict(color=TEXT, size=16),
        ),
        height=390,
        margin=dict(l=15, r=15, t=60, b=30),
        xaxis_title="",
        yaxis_title="R$ por paciente",
        showlegend=False,
        uirevision="flask-chart",
    )

    style_plotly(fig, animated=True)
    return fig


def calculated_table_html(df: pd.DataFrame, render_version: int) -> str:
    """Tabela HTML somente leitura, sem qualquer toolbar."""
    rows = []

    for _, row in df.iterrows():
        product = str(row["Produto"]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        rows.append(
            f"""
            <tr>
                <td class="product">{product}</td>
                <td class="money">{brl(float(row["Custo unitário (R$)"]))}</td>
                <td class="number">{float(row["Qtd/paciente"]):g}</td>
                <td class="money">{brl(float(row["Custo/paciente (R$)"]))}</td>
            </tr>
            """
        )

    return f"""
    <div class="calc-table-wrap" data-render-version="{render_version}">
        <table class="calc-table">
            <thead>
                <tr>
                    <th>Produto</th>
                    <th style="text-align:right">Custo unitário</th>
                    <th style="text-align:right">Qtd/paciente</th>
                    <th style="text-align:right">Custo por paciente</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </div>
    """


# ============================================================
# SESSION STATE
# ============================================================
if "insumos_df" not in st.session_state:
    st.session_state["insumos_df"] = DEFAULT_INPUTS.copy(deep=True)

if "history" not in st.session_state:
    st.session_state["history"] = []

if "editor_version" not in st.session_state:
    st.session_state["editor_version"] = 0

if "editor_message" not in st.session_state:
    st.session_state["editor_message"] = ""

if "calc_view_version" not in st.session_state:
    st.session_state["calc_view_version"] = 0


# ============================================================
# CABEÇALHO
# ============================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Planejamento Financeiro · Botox</div>
        <p class="hero-subtitle">
            Dra. Carolina Bittencourt · Precificação, margem, custos,
            estoque e sustentabilidade financeira em uma única visão.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "💰 Precificação e Lucro por Paciente",
        "📦 Insumos e Custos Editáveis",
        "📈 Análise de Breakeven e Projeções",
        "⚖️ Comparativo de Frascos (100 UI vs 200 UI)",
    ]
)


# ============================================================
# ABA 1 — INPUTS RÁPIDOS
# ============================================================
with tabs[0]:
    section_intro(
        "Visão rápida",
        "Ajuste os principais parâmetros e acompanhe imediatamente custo, preço e lucro por paciente.",
    )

    st.markdown(
        """
        <div class="badge-row" style="margin-bottom:14px;">
            <span class="badge badge-rose">50 UI por aplicação</span>
            <span class="badge badge-gold">Precificação dinâmica</span>
            <span class="badge badge-green">Risco ajustável</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Ajustes rápidos")

    c1, c2, c3 = st.columns([1.05, 1, 1])

    with c1:
        tipo_toxina = st.radio(
            "Frasco usado no procedimento",
            options=["100 UI", "200 UI"],
            horizontal=True,
            key="tipo_toxina",
            help="Somente o frasco selecionado entra no custo do procedimento.",
        )

        frascos_disponiveis = st.number_input(
            "Frascos disponíveis",
            min_value=0,
            value=1,
            step=1,
            key="frascos_disponiveis",
        )

    with c2:
        markup_pct = st.slider(
            "Margem desejada / Markup (%)",
            min_value=50,
            max_value=300,
            value=150,
            step=5,
            key="markup_pct",
            help="Ex.: 150% de markup significa preço = 2,5 × custo.",
        )

        friends_markup_pct = st.slider(
            "Markup Amigos/Família (%)",
            min_value=10,
            max_value=100,
            value=40,
            step=5,
            key="friends_markup_pct",
        )

    with c3:
        risk_pct = st.slider(
            "Reserva de segurança / risco (%)",
            min_value=0,
            max_value=30,
            value=10,
            step=1,
            key="risk_pct",
        )

        dose_ui = st.number_input(
            "Dose por paciente (UI)",
            min_value=1.0,
            max_value=400.0,
            value=50.0,
            step=1.0,
            key="dose_ui",
        )

    with st.expander("Ajustes finos", expanded=False):
        a1, a2, a3 = st.columns(3)

        with a1:
            ajuste_manual = st.number_input(
                "Adicionais por paciente (R$)",
                min_value=0.0,
                value=0.0,
                step=5.0,
                format="%.2f",
                key="ajuste_manual",
            )

        with a2:
            selling_fees_pct = st.slider(
                "Taxas / impostos sobre a venda (%)",
                min_value=0.0,
                max_value=30.0,
                value=0.0,
                step=0.5,
                key="selling_fees_pct",
            )

        with a3:
            rounding_step = st.selectbox(
                "Arredondar preço para",
                options=[1, 5, 10, 25, 50],
                index=2,
                format_func=lambda x: f"R$ {x}",
                key="rounding_step",
            )

    tab1_kpis = st.container()
    tab1_charts = st.container()
    tab1_insights = st.container()


# ============================================================
# ABA 2 — DATA EDITOR COM HISTÓRICO
# ============================================================
with tabs[1]:
    section_intro(
        "Insumos e custos",
        "Edite preços, quantidades e consumo por paciente. Produto e unidade permanecem bloqueados.",
    )

    btn1, btn2, info_col = st.columns([1.15, 1.05, 4.8])

    with btn1:
        if st.button(
            "🔄 Restaurar Padrão",
            use_container_width=True,
            key="restore_default",
            help="Restaura a tabela inicial. O reset também pode ser desfeito.",
        ):
            reset_editor_to_default()
            st.rerun()

    with btn2:
        history_count = len(st.session_state["history"])
        if st.button(
            f"⏮️ Desfazer ({history_count}/10)",
            use_container_width=True,
            key="undo_editor",
            disabled=history_count == 0,
            help="Restaura uma das últimas 10 versões anteriores.",
        ):
            undo_editor()
            st.rerun()

    with info_col:
        if st.session_state.get("editor_message"):
            st.caption(st.session_state["editor_message"])

    st.markdown(
        """
        <div class="editor-tip">
            💡 Dica: as colunas com ícone de lápis / fundo destacado são editáveis.
            <b>Produto</b> e <b>Unidade</b> estão bloqueados.
        </div>
        """,
        unsafe_allow_html=True,
    )

    editor_df = st.session_state["insumos_df"].copy(deep=True)

    editor_key = f"insumos_editor_{st.session_state['editor_version']}"

    edited_df = st.data_editor(
        editor_df,
        key=editor_key,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        column_order=EDITOR_COLUMN_ORDER,
        disabled=["Produto", "Unidade"],
        column_config={
            "Produto": st.column_config.TextColumn(
                "🔒 Produto",
                disabled=True,
                width="large",
                help="Campo fixo.",
            ),
            "Preço compra (R$)": st.column_config.NumberColumn(
                "✏️ Preço de compra",
                min_value=0.0,
                step=0.01,
                format="R$ %.2f",
                disabled=False,
                help="Editável: valor total pago pelo item.",
            ),
            "Qtd total": st.column_config.NumberColumn(
                "✏️ Quantidade total",
                min_value=0.0001,
                step=1.0,
                format="%.2f",
                disabled=False,
                help="Editável: quantidade disponível na embalagem/compra.",
            ),
            "Unidade": st.column_config.TextColumn(
                "🔒 Unidade",
                disabled=True,
                help="Campo fixo.",
            ),
            "Qtd/paciente": st.column_config.NumberColumn(
                "✏️ Uso por paciente",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                disabled=False,
                help="Editável: consumo médio por procedimento.",
            ),
            "Dividido com Julia": st.column_config.CheckboxColumn(
                "✏️ Dividido com Julia",
                disabled=False,
                help="Editável: marque os itens com divisão de desembolso.",
            ),
        },
    )

    # Detecta uma modificação real no st.data_editor.
    # O estado anterior é salvo antes da substituição.
    if not edited_df.equals(editor_df):
        push_history(editor_df)
        st.session_state["insumos_df"] = edited_df.copy(deep=True)
        st.session_state["editor_message"] = "Alteração salva no histórico."
        st.rerun()

    share_carolina_pct = st.slider(
        "Parcela paga pela Dra. Carolina nos itens divididos (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        key="share_carolina_pct",
    )

    tab2_outputs = st.container()


# ============================================================
# ABA 3 — INPUTS DE BREAKEVEN
# ============================================================
with tabs[2]:
    section_intro(
        "Análise de Breakeven e Projeções",
        "Simule custos fixos, volume mensal, recuperação do investimento e resultado operacional.",
    )

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        custo_fixo_mensal = st.number_input(
            "Custos fixos mensais (R$)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            format="%.2f",
            key="custo_fixo_mensal",
        )

    with p2:
        pacientes_mes = st.number_input(
            "Pacientes esperados / mês",
            min_value=0,
            value=10,
            step=1,
            key="pacientes_mes",
        )

    with p3:
        meses_payback = st.number_input(
            "Prazo-alvo de payback (meses)",
            min_value=1,
            max_value=36,
            value=3,
            step=1,
            key="meses_payback",
        )

    with p4:
        meta_resultado_mensal = st.number_input(
            "Meta de resultado mensal (R$)",
            min_value=0.0,
            value=3000.0,
            step=250.0,
            format="%.2f",
            key="meta_resultado_mensal",
        )

    tab3_outputs = st.container()


# ============================================================
# ABA 4 — PREÇO DOS FRASCOS
# ============================================================
with tabs[3]:
    section_intro(
        "Comparativo de Frascos",
        "Compare 100 UI e 200 UI sem misturar as duas opções no custo do procedimento.",
    )

    f1, f2 = st.columns(2)

    with f1:
        preco_toxina_100 = st.number_input(
            "Preço do frasco 100 UI (R$)",
            min_value=0.0,
            value=575.0,
            step=5.0,
            format="%.2f",
            key="preco_toxina_100",
        )

    with f2:
        preco_toxina_200 = st.number_input(
            "Preço do frasco 200 UI (R$)",
            min_value=0.0,
            value=1000.0,
            step=5.0,
            format="%.2f",
            key="preco_toxina_200",
        )

    tab4_outputs = st.container()


# ============================================================
# CÁLCULOS CENTRAIS
# ============================================================
edited = st.session_state["insumos_df"].copy(deep=True)

for numeric_col in ["Preço compra (R$)", "Qtd total", "Qtd/paciente"]:
    edited[numeric_col] = pd.to_numeric(
        edited[numeric_col],
        errors="coerce",
    ).fillna(0.0)

edited["Dividido com Julia"] = (
    edited["Dividido com Julia"].fillna(False).astype(bool)
)

if (edited["Qtd total"] <= 0).any():
    st.error("Todas as quantidades totais precisam ser maiores que zero.")
    st.stop()

edited["Custo unitário (R$)"] = (
    edited["Preço compra (R$)"] / edited["Qtd total"]
)

edited["Custo/paciente (R$)"] = (
    edited["Custo unitário (R$)"] * edited["Qtd/paciente"]
)

preco_toxina = (
    preco_toxina_100
    if tipo_toxina == "100 UI"
    else preco_toxina_200
)

ui_frasco = 100.0 if tipo_toxina == "100 UI" else 200.0

fracao_frasco_paciente = dose_ui / ui_frasco
custo_toxina_paciente = preco_toxina * fracao_frasco_paciente

custo_insumos_sem_toxina = float(
    edited["Custo/paciente (R$)"].sum()
)

custo_base_calculado = (
    custo_insumos_sem_toxina + custo_toxina_paciente
)

custo_base_total = (
    custo_base_calculado + ajuste_manual
)

sigma = risk_pct / 100.0

custo_otimista = custo_base_total
custo_realista = custo_base_total * (1 + sigma)
custo_pessimista = custo_base_total * (1 + 2 * sigma)

fee = selling_fees_pct / 100.0
markup = markup_pct / 100.0
friends_markup = friends_markup_pct / 100.0

preco_novos_raw = (
    custo_realista * (1 + markup) / (1 - fee)
)

preco_amigos_raw = (
    custo_realista * (1 + friends_markup) / (1 - fee)
)

preco_novos = round_up(
    preco_novos_raw,
    float(rounding_step),
)

preco_amigos = round_up(
    preco_amigos_raw,
    float(rounding_step),
)

taxa_novos = preco_novos * fee
taxa_amigos = preco_amigos * fee

lucro_novos = (
    preco_novos
    - taxa_novos
    - custo_realista
)

lucro_amigos = (
    preco_amigos
    - taxa_amigos
    - custo_realista
)

margem_venda_novos = (
    lucro_novos / preco_novos
    if preco_novos > 0
    else np.nan
)

margem_venda_amigos = (
    lucro_amigos / preco_amigos
    if preco_amigos > 0
    else np.nan
)


# ============================================================
# DETALHE DE CUSTOS
# ============================================================
cost_detail = edited[
    [
        "Produto",
        "Custo unitário (R$)",
        "Qtd/paciente",
        "Custo/paciente (R$)",
    ]
].copy()

tox_row = pd.DataFrame(
    [
        {
            "Produto": f"Toxina botulínica · {tipo_toxina}",
            "Custo unitário (R$)": preco_toxina / ui_frasco,
            "Qtd/paciente": dose_ui,
            "Custo/paciente (R$)": custo_toxina_paciente,
        }
    ]
)

cost_detail = pd.concat(
    [cost_detail, tox_row],
    ignore_index=True,
)

if ajuste_manual > 0:
    cost_detail = pd.concat(
        [
            cost_detail,
            pd.DataFrame(
                [
                    {
                        "Produto": "Adicionais manuais",
                        "Custo unitário (R$)": ajuste_manual,
                        "Qtd/paciente": 1.0,
                        "Custo/paciente (R$)": ajuste_manual,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

# A reserva entra no gráfico como componente explícito para que
# a soma da rosca seja igual ao custo realista.
visual_cost_detail = cost_detail.copy()

risk_value = max(
    0.0,
    custo_realista - custo_base_total,
)

if risk_value > 0:
    visual_cost_detail = pd.concat(
        [
            visual_cost_detail,
            pd.DataFrame(
                [
                    {
                        "Produto": "Reserva de segurança",
                        "Custo unitário (R$)": risk_value,
                        "Qtd/paciente": 1.0,
                        "Custo/paciente (R$)": risk_value,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )


# ============================================================
# CENÁRIOS
# ============================================================
scenario_df = pd.DataFrame(
    {
        "Cenário": [
            "Otimista",
            "Realista",
            "Pessimista",
        ],
        "Custo": [
            custo_otimista,
            custo_realista,
            custo_pessimista,
        ],
    }
)

scenario_df["Preço Novos"] = scenario_df["Custo"].apply(
    lambda c: round_up(
        c * (1 + markup) / (1 - fee),
        float(rounding_step),
    )
)

scenario_df["Preço Amigos/Família"] = scenario_df["Custo"].apply(
    lambda c: round_up(
        c * (1 + friends_markup) / (1 - fee),
        float(rounding_step),
    )
)


# ============================================================
# ESTOQUE E INVESTIMENTO
# ============================================================
capacity_rows = []

for _, row in edited.iterrows():
    qpp = float(row["Qtd/paciente"])

    if qpp > 0:
        qty_available = float(row["Qtd total"])

        if bool(row["Dividido com Julia"]):
            qty_available *= share_carolina_pct / 100.0

        capacity = math.floor(
            qty_available / qpp
        )
    else:
        capacity = np.inf

    capacity_rows.append(
        {
            "Produto": row["Produto"],
            "Pacientes suportados": capacity,
        }
    )

tox_capacity = (
    math.floor(
        (frascos_disponiveis * ui_frasco)
        / dose_ui
    )
    if dose_ui > 0
    else 0
)

capacity_rows.append(
    {
        "Produto": f"Toxina botulínica · {tipo_toxina}",
        "Pacientes suportados": tox_capacity,
    }
)

capacity_df = pd.DataFrame(capacity_rows)

finite_capacity = (
    capacity_df
    .replace(np.inf, np.nan)["Pacientes suportados"]
    .dropna()
)

stock_capacity = (
    int(finite_capacity.min())
    if not finite_capacity.empty
    else 0
)

limiting_items = capacity_df[
    capacity_df["Pacientes suportados"]
    == stock_capacity
]["Produto"].tolist()

invest_common_full = float(
    edited["Preço compra (R$)"].sum()
)

invest_toxin_full = (
    preco_toxina * frascos_disponiveis
)

invest_total_full = (
    invest_common_full + invest_toxin_full
)

share = share_carolina_pct / 100.0

carolina_common = float(
    np.where(
        edited["Dividido com Julia"],
        edited["Preço compra (R$)"] * share,
        edited["Preço compra (R$)"],
    ).sum()
)

invest_carolina = (
    carolina_common + invest_toxin_full
)


# ============================================================
# BREAKEVEN
# ============================================================
be_operacional = safe_ceil_div(
    custo_fixo_mensal,
    lucro_novos,
)

parcela_investimento = (
    invest_carolina / meses_payback
)

be_payback = safe_ceil_div(
    custo_fixo_mensal + parcela_investimento,
    lucro_novos,
)

be_caixa_bruto = safe_ceil_div(
    invest_carolina,
    preco_novos,
)

receita_mes = (
    pacientes_mes * preco_novos
)

taxas_mes = (
    receita_mes * fee
)

custo_variavel_mes = (
    pacientes_mes * custo_realista
)

contribuicao_mes = (
    receita_mes
    - taxas_mes
    - custo_variavel_mes
)

resultado_operacional_mes = (
    contribuicao_mes
    - custo_fixo_mensal
)

resultado_apos_payback = (
    resultado_operacional_mes
    - parcela_investimento
)

payback_estimado = (
    invest_carolina / resultado_operacional_mes
    if resultado_operacional_mes > 0
    else np.nan
)

roi_mensal = (
    resultado_operacional_mes / invest_carolina
    if invest_carolina > 0
    else np.nan
)


# ============================================================
# ABA 1 — SAÍDAS
# ============================================================
with tab1_kpis:
    st.markdown("#### Números que importam")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card(
            "Custo do procedimento",
            brl(custo_realista),
            f"Custo base {brl(custo_base_total)} + {risk_pct}% de segurança.",
        )

    with k2:
        kpi_card(
            "Preço sugerido · Novos",
            brl(preco_novos),
            f"Markup de {markup_pct}% · taxas de {selling_fees_pct:.1f}%.",
            variant="highlight",
        )

    with k3:
        kpi_card(
            "Preço · Amigos/Família",
            brl(preco_amigos),
            f"Markup reduzido de {friends_markup_pct}% sobre o custo realista.",
        )

    with k4:
        kpi_card(
            "Lucro por paciente",
            brl(lucro_novos),
            f"Margem sobre a venda: {pct(margem_venda_novos)}.",
            variant="profit",
        )

    # Espaçamento vertical explícito solicitado.
    st.markdown(
        "<div style='margin-bottom: 20px;'></div>",
        unsafe_allow_html=True,
    )

    margin_badge = (
        '<span class="badge badge-green">Margem forte</span>'
        if margem_venda_novos >= 0.60
        else (
            '<span class="badge badge-gold">Margem saudável</span>'
            if margem_venda_novos >= 0.45
            else '<span class="badge badge-rose">Margem de atenção</span>'
        )
    )

    st.markdown(
        f"""
        <div class="kpi-badges">
            {margin_badge}
            <span class="badge badge-neutral">Frasco ativo: {tipo_toxina}</span>
            <span class="badge badge-neutral">{dose_ui:.0f} UI / paciente</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab1_charts:
    st.markdown("#### Leitura visual")

    ch1, ch2 = st.columns([1.02, 1.18])

    with ch1:
        fig_donut = build_donut(
            visual_cost_detail,
            custo_realista,
        )
        st.plotly_chart(
            fig_donut,
            use_container_width=True,
            config=PLOTLY_CONFIG,
            key="cost_donut",
        )

    with ch2:
        fig_scenarios = build_scenario_bars(
            scenario_df
        )
        st.plotly_chart(
            fig_scenarios,
            use_container_width=True,
            config=PLOTLY_CONFIG,
            key="scenario_bars",
        )

with tab1_insights:
    if dose_ui != 50:
        st.warning(
            "A premissa principal informada é de 50 UI por aplicação. "
            "Esta simulação está usando uma dose diferente."
        )

    st.markdown(
        f"""
        <div class="soft-panel">
            <b>Leitura rápida:</b> com o frasco de <b>{tipo_toxina}</b>,
            a toxina representa <b>{brl(custo_toxina_paciente)}</b> por aplicação.
            No cenário realista, o procedimento custa <b>{brl(custo_realista)}</b>
            e gera aproximadamente
            <span class="positive">{brl(lucro_novos)}</span>
            de contribuição por paciente novo.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ABA 2 — TABELA CALCULADA E ESTOQUE
# ============================================================
with tab2_outputs:
    st.markdown("#### Custo calculado por item")

    st.caption(
        "Esta tabela é somente consulta. Ela é recalculada automaticamente a partir dos insumos editáveis."
    )

    reset_col, read_only_col = st.columns([1.35, 5.65])

    with reset_col:
        if st.button(
            "🔄 Resetar Visualização",
            key="reset_calculated_view",
            use_container_width=True,
            help=(
                "Re-renderiza a tabela e recalcula os custos com os dados atuais. "
                "Não altera os valores da tabela de insumos."
            ),
        ):
            st.session_state["calc_view_version"] += 1
            st.toast("Visualização recalculada com os dados atuais.")

    with read_only_col:
        st.markdown(
            """
            <div class="badge-row" style="margin-top:4px;">
                <span class="badge badge-neutral">Somente leitura</span>
                <span class="badge badge-green">Cálculo automático</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        calculated_table_html(
            cost_detail,
            st.session_state["calc_view_version"],
        ),
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns(3)

    with s1:
        kpi_card(
            "Insumos sem toxina",
            brl(custo_insumos_sem_toxina),
            "Materiais de apoio por procedimento.",
        )

    with s2:
        kpi_card(
            "Toxina por paciente",
            brl(custo_toxina_paciente),
            f"{dose_ui:.0f} UI usando frasco de {tipo_toxina}.",
        )

    with s3:
        kpi_card(
            "Capacidade do estoque",
            f"{stock_capacity} pacientes",
            "Limitada pelo item com menor cobertura disponível.",
            variant="highlight",
        )

    if limiting_items:
        st.caption(
            "Gargalo atual de estoque: "
            + ", ".join(limiting_items)
        )

    with st.expander(
        "Ver capacidade estimada de cada item",
        expanded=False,
    ):
        capacity_show = capacity_df.copy()

        capacity_show["Pacientes suportados"] = (
            capacity_show["Pacientes suportados"]
            .apply(
                lambda value: "∞"
                if value == np.inf
                else int(value)
            )
        )

        st.dataframe(
            capacity_show,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# ABA 3 — SAÍDAS
# ============================================================
with tab3_outputs:
    st.markdown("#### Indicadores de sustentabilidade")

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        kpi_card(
            "Investimento inicial",
            brl(invest_carolina),
            "Desembolso estimado da Dra. Carolina.",
        )

    with d2:
        kpi_card(
            "Breakeven operacional",
            f"{be_operacional} pac./mês"
            if be_operacional is not None
            else "—",
            "Volume necessário para cobrir os custos fixos.",
        )

    with d3:
        kpi_card(
            f"BE + payback em {meses_payback} mês(es)",
            f"{be_payback} pac./mês"
            if be_payback is not None
            else "—",
            "Cobre fixos e recupera o investimento no prazo-alvo.",
            variant="highlight",
        )

    with d4:
        kpi_card(
            "Resultado mensal",
            brl(resultado_operacional_mes),
            f"Simulação com {pacientes_mes} pacientes/mês.",
            variant=(
                "profit"
                if resultado_operacional_mes >= 0
                else "default"
            ),
        )

    st.markdown("#### Projeção do mês")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.metric(
            "Receita projetada",
            brl(receita_mes),
        )

    with q2:
        st.metric(
            "Custo variável",
            brl(custo_variavel_mes),
        )

    with q3:
        st.metric(
            "Payback estimado",
            f"{payback_estimado:.1f} meses"
            if np.isfinite(payback_estimado)
            else "—",
        )

    with q4:
        st.metric(
            "ROI mensal estimado",
            pct(roi_mensal)
            if np.isfinite(roi_mensal)
            else "—",
        )

    max_patients_chart = max(
        30,
        int(pacientes_mes * 2),
        (be_payback or 0) + 10,
    )

    patients = np.arange(
        0,
        max_patients_chart + 1,
    )

    profit_curve = (
        patients * preco_novos * (1 - fee)
        - patients * custo_realista
        - custo_fixo_mensal
        - parcela_investimento
    )

    fig_be = build_break_even_chart(
        patients,
        profit_curve,
        be_payback,
    )

    st.plotly_chart(
        fig_be,
        use_container_width=True,
        config=PLOTLY_CONFIG,
        key="breakeven_plot",
    )

    if (
        meta_resultado_mensal > 0
        and resultado_operacional_mes
        >= meta_resultado_mensal
    ):
        st.success(
            f"Meta atingida: a simulação supera "
            f"{brl(meta_resultado_mensal)} de resultado mensal."
        )

        if not st.session_state.get(
            "meta_celebrada",
            False,
        ):
            st.balloons()
            st.session_state[
                "meta_celebrada"
            ] = True
    else:
        st.session_state[
            "meta_celebrada"
        ] = False

    with st.expander(
        "Entender os três pontos de equilíbrio",
        expanded=False,
    ):
        st.markdown(
            f"""
            **Breakeven operacional:** {be_operacional if be_operacional is not None else "—"} pacientes/mês  
            Cobre os custos fixos mensais com a contribuição de cada procedimento.

            **Breakeven com payback:** {be_payback if be_payback is not None else "—"} pacientes/mês  
            Além dos custos fixos, recupera o desembolso inicial em {meses_payback} mês(es).

            **Recuperação simples de caixa:** {be_caixa_bruto if be_caixa_bruto is not None else "—"} pacientes  
            Leitura simplificada do investimento inicial dividido pela receita bruta por procedimento.
            """
        )


# ============================================================
# ABA 4 — COMPARATIVO DE FRASCOS
# ============================================================
comparison = pd.DataFrame(
    [
        {
            "Frasco": "100 UI",
            "Preço do frasco": preco_toxina_100,
            "Custo por UI": (
                preco_toxina_100 / 100.0
                if preco_toxina_100 > 0
                else 0
            ),
            "Custo toxina/paciente": (
                preco_toxina_100
                * dose_ui
                / 100.0
            ),
            "Pacientes teóricos/frasco": (
                math.floor(100.0 / dose_ui)
                if dose_ui > 0
                else 0
            ),
        },
        {
            "Frasco": "200 UI",
            "Preço do frasco": preco_toxina_200,
            "Custo por UI": (
                preco_toxina_200 / 200.0
                if preco_toxina_200 > 0
                else 0
            ),
            "Custo toxina/paciente": (
                preco_toxina_200
                * dose_ui
                / 200.0
            ),
            "Pacientes teóricos/frasco": (
                math.floor(200.0 / dose_ui)
                if dose_ui > 0
                else 0
            ),
        },
    ]
)

comparison["Ativo no cálculo"] = (
    comparison["Frasco"] == tipo_toxina
)

with tab4_outputs:
    best_idx = (
        comparison[
            "Custo toxina/paciente"
        ].idxmin()
    )

    best_row = comparison.loc[
        best_idx
    ]

    a, b, c = st.columns(3)

    with a:
        kpi_card(
            "100 UI · custo/paciente",
            brl(
                comparison.loc[
                    0,
                    "Custo toxina/paciente",
                ]
            ),
            (
                f"{comparison.loc[0, 'Pacientes teóricos/frasco']} "
                "pacientes teóricos por frasco."
            ),
        )

    with b:
        kpi_card(
            "200 UI · custo/paciente",
            brl(
                comparison.loc[
                    1,
                    "Custo toxina/paciente",
                ]
            ),
            (
                f"{comparison.loc[1, 'Pacientes teóricos/frasco']} "
                "pacientes teóricos por frasco."
            ),
        )

    with c:
        economia = abs(
            comparison.loc[
                0,
                "Custo toxina/paciente",
            ]
            - comparison.loc[
                1,
                "Custo toxina/paciente",
            ]
        )

        kpi_card(
            "Melhor custo teórico",
            str(
                best_row["Frasco"]
            ),
            (
                f"Economia de {brl(economia)} "
                "por paciente vs. a outra opção."
            ),
            variant="profit",
        )

    fig_flasks = build_flask_comparison(
        comparison,
        dose_ui,
    )

    st.plotly_chart(
        fig_flasks,
        use_container_width=True,
        config=PLOTLY_CONFIG,
        key="flask_comparison_plot",
    )

    display_comparison = comparison.copy()

    display_comparison[
        "Preço do frasco"
    ] = display_comparison[
        "Preço do frasco"
    ].map(brl)

    display_comparison[
        "Custo por UI"
    ] = display_comparison[
        "Custo por UI"
    ].map(brl)

    display_comparison[
        "Custo toxina/paciente"
    ] = display_comparison[
        "Custo toxina/paciente"
    ].map(brl)

    display_comparison[
        "Ativo no cálculo"
    ] = display_comparison[
        "Ativo no cálculo"
    ].map(
        {
            True: "Sim",
            False: "Não",
        }
    )

    st.dataframe(
        display_comparison,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        f"""
        <div class="soft-panel">
            Com os preços atuais, o frasco de
            <b>{best_row["Frasco"]}</b>
            apresenta o menor custo teórico de toxina por paciente:
            <span class="positive">
                {brl(best_row["Custo toxina/paciente"])}
            </span>.
            A decisão final também deve considerar o aproveitamento real do frasco.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# EXPORTAÇÃO
# ============================================================
summary_export = pd.DataFrame(
    [
        ["Frasco ativo", tipo_toxina],
        ["Dose por paciente (UI)", dose_ui],
        ["Custo base por paciente", custo_base_total],
        ["Custo realista por paciente", custo_realista],
        ["Preço sugerido - novos", preco_novos],
        ["Preço sugerido - amigos/família", preco_amigos],
        ["Lucro por paciente novo", lucro_novos],
        ["Margem sobre venda - novos", margem_venda_novos],
        ["Investimento inicial Dra. Carolina", invest_carolina],
        ["Investimento total em estoque", invest_total_full],
        ["Capacidade estimada do estoque", stock_capacity],
        ["Breakeven operacional", be_operacional],
        ["Breakeven com payback", be_payback],
        ["Pacientes projetados por mês", pacientes_mes],
        ["Resultado operacional mensal", resultado_operacional_mes],
        ["Resultado após parcela de payback", resultado_apos_payback],
    ],
    columns=[
        "Indicador",
        "Valor",
    ],
)

csv = summary_export.to_csv(
    index=False,
    sep=";",
    decimal=",",
).encode("utf-8-sig")

st.divider()

with st.expander(
    "⬇️ Exportar resumo",
    expanded=False,
):
    st.caption(
        "Baixe os principais números da simulação atual em CSV."
    )

    st.download_button(
        "Baixar resumo financeiro",
        data=csv,
        file_name="resumo_financeiro_botox.csv",
        mime="text/csv",
    )

st.caption(
    "Modelo financeiro gerencial. Antes de definir o preço final, "
    "valide custos tributários, política de retoques, desperdício real, "
    "taxas e demais despesas da operação."
)
