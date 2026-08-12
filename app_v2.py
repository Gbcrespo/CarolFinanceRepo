import html
import math
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# CONFIGURAÇÃO GERAL
# =========================================================
st.set_page_config(
    page_title="Planejamento Financeiro UX v2 | Dra. Carolina Bittencourt",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Paleta visual
BG = "#FBF9F7"
CARD = "#FFFFFF"
ROSE = "#E8D5D0"
ROSE_DARK = "#B9867C"
NUDE = "#F2E8E1"
GOLD = "#C7A46A"
TEXT = "#3F3B39"
MUTED = "#7B7470"
GREEN = "#6F9D85"
GREEN_SOFT = "#E4F0E8"
GRAY = "#EEEAE7"
DANGER = "#B36D68"

PLOT_CONFIG = {
    "displayModeBar": False,
    "scrollZoom": False,
    "doubleClick": False,
    "showTips": False,
    "responsive": True,
}


# =========================================================
# CSS CUSTOMIZADO — VISUAL EXECUTIVO / SaaS
# =========================================================
st.markdown(
    f"""
    <style>
        :root {{
            color-scheme: light !important;
        }}

        html, body, [data-testid="stAppViewContainer"], .stApp {{
            background: {BG} !important;
            color: {TEXT} !important;
            color-scheme: light !important;
        }}

        .block-container {{
            max-width: 1480px;
            padding-top: 1.7rem;
            padding-bottom: 2.5rem;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT} !important;
            letter-spacing: -0.02em;
        }}

        p, label, .stMarkdown, [data-testid="stCaptionContainer"] {{
            color: {TEXT};
        }}

        /* Cabeçalho */
        .hero {{
            background: linear-gradient(135deg, #FFFDFC 0%, {NUDE} 100%);
            border: 1px solid #EEE4DE;
            border-radius: 20px;
            padding: 26px 30px;
            margin-bottom: 1.15rem;
            box-shadow: 0 10px 30px rgba(91, 70, 60, 0.06);
        }}

        .hero-title {{
            font-size: 2.0rem;
            font-weight: 750;
            line-height: 1.15;
            color: {TEXT};
            margin-bottom: 8px;
        }}

        .hero-subtitle {{
            font-size: 0.98rem;
            color: {MUTED};
            margin: 0;
        }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 650;
            margin-right: 6px;
            margin-bottom: 6px;
            border: 1px solid transparent;
        }}

        .badge-rose {{
            background: #F5E8E4;
            color: #9A675F;
            border-color: #ECD7D1;
        }}

        .badge-gold {{
            background: #F8F0E2;
            color: #8D7042;
            border-color: #EEDDBF;
        }}

        .badge-green {{
            background: {GREEN_SOFT};
            color: #4E7561;
            border-color: #D3E7DA;
        }}

        .badge-neutral {{
            background: #F3F1EF;
            color: #6C6662;
            border-color: #E6E2DF;
        }}

        .kpi-badges {{
            margin-top: 18px;
            margin-bottom: 14px;
        }}

        /* Cards KPI */
        .kpi-card {{
            background: {CARD};
            border: 1px solid #EEE8E4;
            border-radius: 16px;
            padding: 20px 20px 18px 20px;
            min-height: 145px;
            box-shadow: 0 7px 22px rgba(76, 61, 54, 0.055);
            transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 13px 28px rgba(76, 61, 54, 0.10);
            border-color: #E3D4CD;
        }}

        .kpi-highlight {{
            background: linear-gradient(145deg, #FFFFFF 0%, #FBF5F2 100%);
        }}

        .kpi-profit {{
            background: linear-gradient(145deg, #FFFFFF 0%, {GREEN_SOFT} 100%);
            border-color: #DCE9E0;
        }}

        .kpi-label {{
            color: {MUTED};
            font-size: 0.80rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.055em;
            margin-bottom: 10px;
        }}

        .kpi-value {{
            color: {TEXT};
            font-size: 1.62rem;
            font-weight: 780;
            line-height: 1.1;
            margin-bottom: 9px;
        }}

        .kpi-sub {{
            color: {MUTED};
            font-size: 0.82rem;
            line-height: 1.35;
        }}

        .positive {{
            color: {GREEN};
            font-weight: 700;
        }}

        /* Cards de seção */
        .soft-panel {{
            background: rgba(255, 255, 255, 0.80);
            border: 1px solid #EEE8E4;
            border-radius: 16px;
            padding: 18px 20px;
            margin: 8px 0 14px 0;
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            border-radius: 10px 10px 0 0;
            padding-left: 16px;
            padding-right: 16px;
            font-weight: 650;
            color: {TEXT} !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            background: #F3E9E5 !important;
            color: #8E625A !important;
        }}

        div[data-baseweb="tab-border"] {{
            background-color: #E8DDD7;
        }}

        /* ----------------------------
           CORREÇÃO DE COMPONENTES ESCUROS
           ---------------------------- */
        [data-testid="stExpander"] {{
            background: #FFFFFF !important;
            border: 1px solid #E9E1DC !important;
            border-radius: 14px !important;
            overflow: hidden;
        }}

        [data-testid="stExpander"] details,
        [data-testid="stExpander"] summary {{
            background: #FFFFFF !important;
            color: {TEXT} !important;
        }}

        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary svg {{
            color: {TEXT} !important;
            fill: {TEXT} !important;
        }}

        [data-testid="stExpander"] > details > div {{
            background: #FFFDFC !important;
        }}

        [data-testid="stNumberInput"] [data-baseweb="input"],
        [data-testid="stTextInput"] [data-baseweb="input"] {{
            background: #FFFFFF !important;
            border-color: #DDD4CF !important;
            border-radius: 10px !important;
        }}

        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input {{
            background: #FFFFFF !important;
            color: {TEXT} !important;
            -webkit-text-fill-color: {TEXT} !important;
        }}

        [data-testid="stNumberInput"] button {{
            background: #F7F3F0 !important;
            color: {TEXT} !important;
            border-color: #E7DFDA !important;
        }}

        [data-testid="stNumberInput"] button svg {{
            fill: {TEXT} !important;
            color: {TEXT} !important;
        }}

        div[data-baseweb="select"] > div {{
            background: #FFFFFF !important;
            color: {TEXT} !important;
            border-color: #DDD4CF !important;
            border-radius: 10px !important;
        }}

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] svg {{
            color: {TEXT} !important;
            fill: {TEXT} !important;
        }}

        [data-baseweb="popover"],
        [data-baseweb="popover"] > div,
        ul[role="listbox"] {{
            background: #FFFFFF !important;
            color: {TEXT} !important;
        }}

        li[role="option"] {{
            background: #FFFFFF !important;
            color: {TEXT} !important;
        }}

        li[role="option"]:hover {{
            background: #F6EFEB !important;
            color: {TEXT} !important;
        }}

        [data-testid="stRadio"] label,
        [data-testid="stCheckbox"] label,
        [data-testid="stSlider"] label,
        [data-testid="stNumberInput"] label,
        [data-testid="stSelectbox"] label {{
            color: {TEXT} !important;
        }}

        [data-testid="stSlider"] [data-baseweb="slider"] * {{
            color: {TEXT};
        }}

        /* Botões */
        .stButton > button,
        .stDownloadButton > button {{
            border-radius: 10px !important;
            border: 1px solid #D9CCC4 !important;
            background: #FFFDFB !important;
            color: {TEXT} !important;
            font-weight: 650 !important;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            border-color: {ROSE_DARK} !important;
            color: #8E625A !important;
            background: #FBF4F1 !important;
        }}

        /* ----------------------------
           EDITOR DE INSUMOS CUSTOMIZADO
           ---------------------------- */
        .editor-help {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0 14px 0;
        }}

        .editor-head {{
            font-size: 0.76rem;
            color: {MUTED};
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: .045em;
            padding: 0 3px 7px 3px;
        }}

        .locked-cell {{
            background: #F4F1EF;
            color: #5E5854;
            border: 1px solid #E7E1DD;
            border-radius: 10px;
            min-height: 40px;
            padding: 9px 10px;
            display: flex;
            align-items: center;
            font-size: 0.88rem;
            font-weight: 600;
        }}

        .locked-cell.unit {{
            font-weight: 500;
            color: {MUTED};
        }}

        .editor-separator {{
            height: 1px;
            background: #F0EBE8;
            margin: 3px 0 7px 0;
        }}

        /* Tabela calculada - intencionalmente diferente do editor */
        .calc-table-wrap {{
            background: #FFFFFF;
            border: 1px solid #E9E2DE;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 6px 18px rgba(72, 60, 53, 0.045);
            margin-top: 8px;
            margin-bottom: 18px;
        }}

        .calc-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.87rem;
        }}

        .calc-table thead th {{
            background: #F1EBE7;
            color: #665E59;
            text-align: left;
            padding: 12px 14px;
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: .045em;
            font-weight: 750;
            border-bottom: 1px solid #E2D9D4;
        }}

        .calc-table tbody td {{
            padding: 11px 14px;
            color: {TEXT};
            border-bottom: 1px solid #F0EBE8;
        }}

        .calc-table tbody tr:nth-child(even) {{
            background: #FCFAF8;
        }}

        .calc-table tbody tr:last-child td {{
            border-bottom: none;
        }}

        .calc-table .money {{
            text-align: right;
            font-variant-numeric: tabular-nums;
            font-weight: 650;
        }}

        .calc-table .qty {{
            text-align: right;
            font-variant-numeric: tabular-nums;
        }}

        .calc-table .product {{
            font-weight: 650;
        }}

        /* ----------------------------
           DONUT SEM NAVEGAÇÃO
           ---------------------------- */
        .donut-card {{
            background: #FFFFFF;
            border: 1px solid #EEE8E4;
            border-radius: 16px;
            padding: 18px;
            min-height: 430px;
            box-shadow: 0 6px 18px rgba(72, 60, 53, 0.045);
        }}

        .visual-title {{
            font-size: 1.03rem;
            font-weight: 750;
            color: {TEXT};
            margin-bottom: 4px;
        }}

        .visual-subtitle {{
            color: {MUTED};
            font-size: 0.79rem;
            margin-bottom: 14px;
        }}

        .donut-layout {{
            display: grid;
            grid-template-columns: 220px 1fr;
            gap: 18px;
            align-items: center;
        }}

        .cost-donut {{
            width: 210px;
            height: 210px;
            border-radius: 50%;
            position: relative;
            margin: 0 auto;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,.45);
        }}

        .donut-hole {{
            position: absolute;
            inset: 44px;
            background: #FFFFFF;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 0 1px #F0EBE8;
            text-align: center;
            padding: 8px;
        }}

        .donut-hole strong {{
            font-size: 1.02rem;
            color: {TEXT};
        }}

        .donut-hole span {{
            font-size: .71rem;
            color: {MUTED};
            margin-top: 4px;
        }}

        .cost-legend {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            column-gap: 14px;
            row-gap: 7px;
        }}

        .cost-legend-item {{
            display: grid;
            grid-template-columns: 10px minmax(0, 1fr) auto;
            gap: 7px;
            align-items: center;
            min-width: 0;
            padding-bottom: 4px;
            border-bottom: 1px solid #F3EFEC;
        }}

        .cost-dot {{
            width: 9px;
            height: 9px;
            border-radius: 50%;
        }}

        .cost-name {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: .72rem;
            color: #5A5551;
        }}

        .cost-pct {{
            font-size: .72rem;
            color: {TEXT};
            font-weight: 750;
            font-variant-numeric: tabular-nums;
        }}

        .cost-value {{
            display: block;
            font-size: .64rem;
            color: {MUTED};
            font-weight: 500;
            margin-top: 1px;
        }}

        @media (max-width: 900px) {{
            .hero-title {{
                font-size: 1.55rem;
            }}
            .kpi-card {{
                min-height: 125px;
                margin-bottom: 8px;
            }}
            .donut-layout {{
                grid-template-columns: 1fr;
            }}
            .cost-legend {{
                grid-template-columns: 1fr;
            }}
        }}

        hr {{
            border-color: #EEE8E4;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DADOS INICIAIS
# =========================================================
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

EDITOR_COLUMNS = ["Preço compra (R$)", "Qtd total", "Qtd/paciente", "Dividido com Julia"]


# =========================================================
# HELPERS
# =========================================================
def brl(value: float) -> str:
    if value is None or not np.isfinite(value):
        return "—"
    s = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


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
    css_variant = ""
    if variant == "highlight":
        css_variant = "kpi-highlight"
    elif variant == "profit":
        css_variant = "kpi-profit"

    st.markdown(
        f"""
        <div class="kpi-card {css_variant}">
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


def editor_key(row_idx: int, field: str) -> str:
    safe = (
        field.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("$", "")
    )
    return f"insumo_{row_idx}_{safe}"


def sync_editor_widgets_from_df() -> None:
    """Sincroniza widgets do editor após reset/undo."""
    df = st.session_state["insumos_df"]
    for idx, row in df.iterrows():
        st.session_state[editor_key(idx, "Preço compra (R$)")] = float(row["Preço compra (R$)"])
        st.session_state[editor_key(idx, "Qtd total")] = float(row["Qtd total"])
        st.session_state[editor_key(idx, "Qtd/paciente")] = float(row["Qtd/paciente"])
        st.session_state[editor_key(idx, "Dividido com Julia")] = bool(row["Dividido com Julia"])


def push_history() -> None:
    history = st.session_state.setdefault("insumos_history", [])
    history.append(st.session_state["insumos_df"].copy(deep=True))
    st.session_state["insumos_history"] = history[-10:]


def update_insumo_value(row_idx: int, field: str, widget_key: str) -> None:
    """Registra uma ação e atualiza uma célula editável."""
    new_value = st.session_state[widget_key]
    current_value = st.session_state["insumos_df"].at[row_idx, field]

    # Evita criar histórico quando o valor não mudou de fato.
    if isinstance(current_value, (float, np.floating)):
        if math.isclose(float(current_value), float(new_value), rel_tol=0, abs_tol=1e-12):
            return
    elif current_value == new_value:
        return

    push_history()
    updated = st.session_state["insumos_df"].copy(deep=True)
    updated.at[row_idx, field] = new_value
    st.session_state["insumos_df"] = updated
    st.session_state["last_insumo_action"] = (
        f"{updated.at[row_idx, 'Produto']} · {field} atualizado"
    )


def reset_insumos() -> None:
    push_history()
    st.session_state["insumos_df"] = DEFAULT_INPUTS.copy(deep=True)
    sync_editor_widgets_from_df()
    st.session_state["last_insumo_action"] = "Valores originais restaurados"


def undo_insumo_action() -> None:
    history = st.session_state.get("insumos_history", [])
    if not history:
        return
    previous = history.pop()
    st.session_state["insumos_history"] = history
    st.session_state["insumos_df"] = previous.copy(deep=True)
    sync_editor_widgets_from_df()
    st.session_state["last_insumo_action"] = "Última alteração desfeita"


def calculated_table_html(df: pd.DataFrame) -> str:
    rows = []
    for _, row in df.iterrows():
        rows.append(
            f"""
            <tr>
                <td class="product">{html.escape(str(row["Produto"]))}</td>
                <td class="money">{brl(float(row["Custo unitário (R$)"]))}</td>
                <td class="qty">{float(row["Qtd/paciente"]):g}</td>
                <td class="money">{brl(float(row["Custo/paciente (R$)"]))}</td>
            </tr>
            """
        )

    return f"""
    <div class="calc-table-wrap">
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


def donut_html(cost_df: pd.DataFrame, total_realista: float) -> str:
    """
    Donut sem navegação/zoom.
    A contingência aparece como componente próprio para o total do gráfico
    coincidir com o custo realista.
    """
    df = cost_df.copy()
    df = df[df["Custo/paciente (R$)"] > 0].copy()
    df = df.sort_values("Custo/paciente (R$)", ascending=False).reset_index(drop=True)

    total = float(df["Custo/paciente (R$)"].sum())
    if total <= 0:
        return "<div class='donut-card'>Sem custos para exibir.</div>"

    colors = [
        "#C7A46A", "#B9867C", "#6F9D85", "#D8B8AE", "#A9B9AF", "#D6C6B7",
        "#C4BBB5", "#E4CFC6", "#8FA79A", "#D5AFA9", "#BDA47C", "#C9D1CB",
        "#E3D6CA", "#9E8D82",
    ]

    stops = []
    legend = []
    start = 0.0

    for i, row in df.iterrows():
        value = float(row["Custo/paciente (R$)"])
        share = value / total
        end = start + share * 360
        color = colors[i % len(colors)]
        stops.append(f"{color} {start:.3f}deg {end:.3f}deg")
        product = html.escape(str(row["Produto"]))
        legend.append(
            f"""
            <div class="cost-legend-item" title="{product}">
                <span class="cost-dot" style="background:{color}"></span>
                <span class="cost-name">
                    {product}
                    <span class="cost-value">{brl(value)}</span>
                </span>
                <span class="cost-pct">{share * 100:.2f}%</span>
            </div>
            """
        )
        start = end

    return f"""
    <div class="donut-card">
        <div class="visual-title">Composição do custo realista</div>
        <div class="visual-subtitle">
            Todos os itens aparecem na legenda com valor e participação percentual.
        </div>
        <div class="donut-layout">
            <div class="cost-donut" style="background:conic-gradient({','.join(stops)})">
                <div class="donut-hole">
                    <strong>{brl(total_realista)}</strong>
                    <span>custo realista</span>
                </div>
            </div>
            <div class="cost-legend">
                {''.join(legend)}
            </div>
        </div>
    </div>
    """


def animated_scenario_bars(
    scenario_df: pd.DataFrame,
    state_key: str = "prev_scenario_chart",
) -> None:
    """
    Gráfico de barras HTML/CSS:
    - sem zoom, pan, modebar ou navegação;
    - valores e legenda ficam sempre visíveis;
    - anima do valor anterior para o novo em cada atualização.
    """
    indicators = ["Custo", "Preço Novos", "Preço Amigos/Família"]
    labels = {
        "Custo": "Custo",
        "Preço Novos": "Novos pacientes",
        "Preço Amigos/Família": "Amigos/Família",
    }
    colors = {
        "Custo": "#C9C1BC",
        "Preço Novos": "#B9867C",
        "Preço Amigos/Família": "#C7A46A",
    }

    current = {}
    for _, row in scenario_df.iterrows():
        for indicator in indicators:
            current[f"{row['Cenário']}|{indicator}"] = float(row[indicator])

    previous = st.session_state.get(state_key, {})
    max_value = max(max(current.values()), 1)
    axis_max = max(100.0, math.ceil(max_value / 100.0) * 100.0)

    legend_html = "".join(
        f"""
        <div class="legend-item">
            <span class="legend-dot" style="background:{colors[ind]}"></span>
            {labels[ind]}
        </div>
        """
        for ind in indicators
    )

    groups_html = []
    for _, row in scenario_df.iterrows():
        scenario = str(row["Cenário"])
        bars = []
        for indicator in indicators:
            key = f"{scenario}|{indicator}"
            cur = float(current[key])
            prev = float(previous.get(key, 0.0))
            cur_h = max(1.5, min(100.0, cur / axis_max * 100.0))
            prev_h = max(0.0, min(100.0, prev / axis_max * 100.0))
            bars.append(
                f"""
                <div class="bar-slot">
                    <div
                        class="bar"
                        style="
                            --from:{prev_h:.3f}%;
                            --to:{cur_h:.3f}%;
                            background:{colors[indicator]};
                        "
                        title="{labels[indicator]} · {scenario}: {brl(cur)}"
                    >
                        <span class="bar-value">{brl(cur)}</span>
                    </div>
                </div>
                """
            )

        groups_html.append(
            f"""
            <div class="group">
                <div class="bars">{''.join(bars)}</div>
                <div class="group-label">{html.escape(scenario)}</div>
            </div>
            """
        )

    chart_html = f"""
    <html>
    <head>
    <style>
        * {{ box-sizing:border-box; }}
        body {{
            margin:0;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color:{TEXT};
            background:transparent;
        }}
        .card {{
            height:430px;
            background:#FFFFFF;
            border:1px solid #EEE8E4;
            border-radius:16px;
            padding:18px 18px 14px 18px;
            box-shadow:0 6px 18px rgba(72,60,53,.045);
            overflow:hidden;
        }}
        .title {{
            font-size:16px;
            font-weight:750;
            margin-bottom:4px;
        }}
        .subtitle {{
            color:{MUTED};
            font-size:12.5px;
            margin-bottom:12px;
        }}
        .legend {{
            display:flex;
            flex-wrap:wrap;
            gap:14px;
            margin:2px 0 20px 0;
            font-size:12px;
            color:#5E5854;
        }}
        .legend-item {{
            display:flex;
            align-items:center;
            gap:6px;
            font-weight:650;
        }}
        .legend-dot {{
            width:10px;
            height:10px;
            border-radius:3px;
        }}
        .plot {{
            position:relative;
            height:300px;
            padding:12px 10px 0 42px;
        }}
        .grid {{
            position:absolute;
            inset:0 0 35px 42px;
            border-bottom:1px solid #D9D2CD;
            background:
                repeating-linear-gradient(
                    to top,
                    transparent 0,
                    transparent calc(25% - 1px),
                    #EEE9E6 calc(25% - 1px),
                    #EEE9E6 25%
                );
        }}
        .axis-label {{
            position:absolute;
            left:0;
            width:36px;
            text-align:right;
            font-size:10px;
            color:#918985;
            transform:translateY(50%);
        }}
        .groups {{
            position:absolute;
            inset:12px 10px 35px 42px;
            display:flex;
            align-items:stretch;
            justify-content:space-around;
            gap:18px;
        }}
        .group {{
            flex:1;
            display:flex;
            flex-direction:column;
            min-width:0;
        }}
        .bars {{
            height:100%;
            display:flex;
            justify-content:center;
            align-items:flex-end;
            gap:9px;
            min-width:0;
        }}
        .bar-slot {{
            height:100%;
            width:25%;
            min-width:34px;
            max-width:58px;
            display:flex;
            align-items:flex-end;
        }}
        .bar {{
            width:100%;
            height:var(--from);
            border-radius:7px 7px 2px 2px;
            position:relative;
            animation:barMove 760ms cubic-bezier(.22,.8,.32,1) forwards;
            box-shadow:0 3px 10px rgba(55,45,40,.08);
        }}
        .bar-value {{
            position:absolute;
            top:-24px;
            left:50%;
            transform:translateX(-50%);
            font-size:10px;
            color:{TEXT};
            font-weight:750;
            white-space:nowrap;
        }}
        .group-label {{
            margin-top:10px;
            text-align:center;
            font-size:12px;
            font-weight:650;
            color:#6A635E;
            white-space:nowrap;
        }}
        @keyframes barMove {{
            from {{ height:var(--from); }}
            to {{ height:var(--to); }}
        }}
        @media (max-width:700px) {{
            .bar-slot {{ min-width:22px; }}
            .bar-value {{ font-size:9px; }}
            .group-label {{ font-size:10px; }}
        }}
    </style>
    </head>
    <body>
        <div class="card">
            <div class="title">Precificação por cenário</div>
            <div class="subtitle">Valores sempre visíveis · sem zoom ou navegação dentro do gráfico.</div>
            <div class="legend">{legend_html}</div>
            <div class="plot">
                <div class="grid"></div>
                <div class="axis-label" style="bottom:35px;">R$ 0</div>
                <div class="axis-label" style="bottom:calc(25% + 26px);">{brl(axis_max * .25).replace("R$ ", "")}</div>
                <div class="axis-label" style="bottom:calc(50% + 17px);">{brl(axis_max * .50).replace("R$ ", "")}</div>
                <div class="axis-label" style="bottom:calc(75% + 8px);">{brl(axis_max * .75).replace("R$ ", "")}</div>
                <div class="axis-label" style="top:-1px;">{brl(axis_max).replace("R$ ", "")}</div>
                <div class="groups">{''.join(groups_html)}</div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(chart_html, height=440, scrolling=False)
    st.session_state[state_key] = current


def animated_two_bars(
    labels: list[str],
    values: list[float],
    colors: list[str],
    title: str,
    subtitle: str,
    state_key: str,
) -> None:
    current = {label: float(value) for label, value in zip(labels, values)}
    previous = st.session_state.get(state_key, {})
    max_value = max(max(values), 1)
    axis_max = max(50.0, math.ceil(max_value / 50.0) * 50.0)

    bars = []
    for label, value, color in zip(labels, values, colors):
        prev = float(previous.get(label, 0.0))
        cur_h = max(2.0, min(100.0, value / axis_max * 100.0))
        prev_h = max(0.0, min(100.0, prev / axis_max * 100.0))
        bars.append(
            f"""
            <div class="item">
                <div class="bar-area">
                    <div class="bar" style="--from:{prev_h:.3f}%;--to:{cur_h:.3f}%;background:{color};">
                        <div class="value">{brl(value)}</div>
                    </div>
                </div>
                <div class="label">{html.escape(label)}</div>
            </div>
            """
        )

    chart_html = f"""
    <html><head><style>
    *{{box-sizing:border-box}}
    body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:transparent;color:{TEXT}}}
    .card{{height:380px;background:#fff;border:1px solid #EEE8E4;border-radius:16px;padding:18px;box-shadow:0 6px 18px rgba(72,60,53,.045)}}
    .title{{font-size:16px;font-weight:750;margin-bottom:4px}}
    .subtitle{{font-size:12.5px;color:{MUTED};margin-bottom:16px}}
    .chart{{height:285px;display:flex;justify-content:center;align-items:stretch;gap:55px;border-bottom:1px solid #D8D1CC;background:repeating-linear-gradient(to top,transparent 0,transparent calc(25% - 1px),#F0EBE8 calc(25% - 1px),#F0EBE8 25%);padding:10px 30px 0 30px}}
    .item{{width:150px;height:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center}}
    .bar-area{{width:84px;height:245px;display:flex;align-items:flex-end}}
    .bar{{width:100%;height:var(--from);border-radius:10px 10px 3px 3px;position:relative;animation:move 760ms cubic-bezier(.22,.8,.32,1) forwards;box-shadow:0 4px 12px rgba(55,45,40,.08)}}
    .value{{position:absolute;top:-29px;left:50%;transform:translateX(-50%);font-size:12px;font-weight:750;white-space:nowrap;color:{TEXT}}}
    .label{{font-size:12px;font-weight:700;margin-top:8px;color:#655E59}}
    @keyframes move{{from{{height:var(--from)}}to{{height:var(--to)}}}}
    </style></head><body>
    <div class="card">
        <div class="title">{html.escape(title)}</div>
        <div class="subtitle">{html.escape(subtitle)}</div>
        <div class="chart">{''.join(bars)}</div>
    </div>
    </body></html>
    """
    components.html(chart_html, height=390, scrolling=False)
    st.session_state[state_key] = current


# =========================================================
# SESSION STATE — EDITOR COM RESET E UNDO (10 AÇÕES)
# =========================================================
if "insumos_df" not in st.session_state:
    st.session_state["insumos_df"] = DEFAULT_INPUTS.copy(deep=True)

if "insumos_history" not in st.session_state:
    st.session_state["insumos_history"] = []

if "last_insumo_action" not in st.session_state:
    st.session_state["last_insumo_action"] = ""


# =========================================================
# CABEÇALHO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div style="margin-bottom:10px;">
            <span class="badge badge-green">UX v2 · gráficos e tabelas revisados</span>
        </div>
        <div class="hero-title">Planejamento Financeiro · Botox</div>
        <p class="hero-subtitle">
            Dra. Carolina Bittencourt · Uma visão simples para decidir preço,
            acompanhar margem e planejar o crescimento do serviço.
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


# =========================================================
# ABA 1 — INPUTS RÁPIDOS
# =========================================================
with tabs[0]:
    section_intro(
        "Visão rápida",
        "Ajuste os controles principais e veja imediatamente o custo, o preço e o lucro estimado por paciente.",
    )

    st.markdown(
        '<span class="badge badge-rose">50 UI por aplicação</span>'
        '<span class="badge badge-gold">Precificação dinâmica</span>'
        '<span class="badge badge-green">Risco ajustável</span>',
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
            help="Somente o frasco selecionado entra no cálculo do procedimento.",
        )
        frascos_disponiveis = st.number_input(
            "Frascos disponíveis",
            min_value=0,
            value=1,
            step=1,
            key="frascos_disponiveis",
            help="Quantidade do frasco selecionado atualmente disponível.",
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
            help="Mantém um preço reduzido sem vender abaixo do custo realista.",
        )

    with c3:
        risk_pct = st.slider(
            "Reserva de segurança / risco (%)",
            min_value=0,
            max_value=30,
            value=10,
            step=1,
            key="risk_pct",
            help="Proteção para perdas, variação de dose, desperdício e retoques.",
        )
        dose_ui = st.number_input(
            "Dose por paciente (UI)",
            min_value=1.0,
            max_value=400.0,
            value=50.0,
            step=1.0,
            key="dose_ui",
            help="A premissa padrão informada é de 50 UI por aplicação.",
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
                help="Descarte, retoques previstos, deslocamento ou itens não listados.",
            )
        with a2:
            selling_fees_pct = st.slider(
                "Taxas / impostos sobre a venda (%)",
                min_value=0.0,
                max_value=30.0,
                value=0.0,
                step=0.5,
                key="selling_fees_pct",
                help="Ex.: cartão, imposto, comissão ou taxa proporcional ao preço cobrado.",
            )
        with a3:
            rounding_step = st.selectbox(
                "Arredondar preço para",
                options=[1, 5, 10, 25, 50],
                index=2,
                key="rounding_step",
                format_func=lambda x: f"R$ {x}",
                help="Arredondamento comercial sempre para cima.",
            )

    tab1_kpis = st.container()
    tab1_charts = st.container()
    tab1_insights = st.container()


# =========================================================
# ABA 2 — EDITOR CUSTOMIZADO
# =========================================================
with tabs[1]:
    section_intro(
        "Insumos e custos",
        "Somente os campos marcados com ✎ são editáveis. Produto e unidade são fixos e aparecem em cinza.",
    )

    toolbar1, toolbar2, toolbar3 = st.columns([1.1, 1.1, 4.8])
    with toolbar1:
        st.button(
            "↺ Restaurar originais",
            on_click=reset_insumos,
            key="reset_insumos_top",
            use_container_width=True,
            help="Restaura todos os preços, quantidades e usos para os valores iniciais.",
        )
    with toolbar2:
        history_count = len(st.session_state.get("insumos_history", []))
        st.button(
            f"↶ Desfazer ({history_count}/10)",
            on_click=undo_insumo_action,
            key="undo_insumos_top",
            use_container_width=True,
            disabled=history_count == 0,
            help="Desfaz até as 10 últimas alterações feitas na grade.",
        )
    with toolbar3:
        if st.session_state.get("last_insumo_action"):
            st.caption(f"Última ação: {st.session_state['last_insumo_action']}")

    st.markdown(
        """
        <div class="editor-help">
            <span class="badge badge-rose">✎ Editável: preço, quantidade, uso e divisão</span>
            <span class="badge badge-neutral">🔒 Fixo: produto e unidade</span>
            <span class="badge badge-green">↶ Histórico: até 10 alterações</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    head_cols = st.columns([2.2, 1.2, 1.1, 0.9, 1.1, 1.05])
    headers = [
        "🔒 Produto",
        "✎ Preço de compra",
        "✎ Quantidade total",
        "🔒 Unidade",
        "✎ Uso/paciente",
        "✎ Dividido c/ Julia",
    ]
    for col, title in zip(head_cols, headers):
        col.markdown(f'<div class="editor-head">{title}</div>', unsafe_allow_html=True)

    current_df = st.session_state["insumos_df"]

    for idx, row in current_df.iterrows():
        row_cols = st.columns([2.2, 1.2, 1.1, 0.9, 1.1, 1.05], vertical_alignment="center")

        with row_cols[0]:
            st.markdown(
                f'<div class="locked-cell">{html.escape(str(row["Produto"]))}</div>',
                unsafe_allow_html=True,
            )

        price_key = editor_key(idx, "Preço compra (R$)")
        qty_key = editor_key(idx, "Qtd total")
        use_key = editor_key(idx, "Qtd/paciente")
        julia_key = editor_key(idx, "Dividido com Julia")

        with row_cols[1]:
            st.number_input(
                f"Preço {row['Produto']}",
                min_value=0.0,
                value=float(row["Preço compra (R$)"]),
                step=0.01,
                format="%.2f",
                key=price_key,
                label_visibility="collapsed",
                on_change=update_insumo_value,
                args=(idx, "Preço compra (R$)", price_key),
            )

        with row_cols[2]:
            st.number_input(
                f"Quantidade {row['Produto']}",
                min_value=0.0001,
                value=float(row["Qtd total"]),
                step=1.0,
                format="%.2f",
                key=qty_key,
                label_visibility="collapsed",
                on_change=update_insumo_value,
                args=(idx, "Qtd total", qty_key),
            )

        with row_cols[3]:
            st.markdown(
                f'<div class="locked-cell unit">{html.escape(str(row["Unidade"]))}</div>',
                unsafe_allow_html=True,
            )

        with row_cols[4]:
            st.number_input(
                f"Uso {row['Produto']}",
                min_value=0.0,
                value=float(row["Qtd/paciente"]),
                step=0.01,
                format="%.2f",
                key=use_key,
                label_visibility="collapsed",
                on_change=update_insumo_value,
                args=(idx, "Qtd/paciente", use_key),
            )

        with row_cols[5]:
            st.checkbox(
                f"Dividir {row['Produto']}",
                value=bool(row["Dividido com Julia"]),
                key=julia_key,
                label_visibility="collapsed",
                on_change=update_insumo_value,
                args=(idx, "Dividido com Julia", julia_key),
            )

        st.markdown('<div class="editor-separator"></div>', unsafe_allow_html=True)

    share_carolina_pct = st.slider(
        "Parcela paga pela Dra. Carolina nos itens divididos (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        key="share_carolina_pct",
        help="Ex.: 50% significa que metade do desembolso inicial do item é da Dra. Carolina.",
    )

    tab2_outputs = st.container()


# =========================================================
# ABA 3 — INPUTS AVANÇADOS
# =========================================================
with tabs[2]:
    section_intro(
        "Análise profunda & breakeven",
        "Use esta área para avaliar volume mensal, retorno do investimento e metas de resultado.",
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


# =========================================================
# ABA 4 — PREÇOS DE FRASCOS
# =========================================================
with tabs[3]:
    section_intro(
        "Eficiência dos frascos",
        "Compare custo por UI, custo de toxina por paciente e aproveitamento teórico de cada apresentação.",
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


# =========================================================
# CÁLCULOS CENTRAIS
# =========================================================
edited = st.session_state["insumos_df"].copy(deep=True)

for col in ["Preço compra (R$)", "Qtd total", "Qtd/paciente"]:
    edited[col] = pd.to_numeric(edited[col], errors="coerce").fillna(0.0)

edited["Dividido com Julia"] = edited["Dividido com Julia"].fillna(False).astype(bool)

if (edited["Qtd total"] <= 0).any():
    st.error("A quantidade total de todos os insumos deve ser maior que zero.")
    st.stop()

edited["Custo unitário (R$)"] = edited["Preço compra (R$)"] / edited["Qtd total"]
edited["Custo/paciente (R$)"] = edited["Custo unitário (R$)"] * edited["Qtd/paciente"]

preco_toxina = preco_toxina_100 if tipo_toxina == "100 UI" else preco_toxina_200
ui_frasco = 100.0 if tipo_toxina == "100 UI" else 200.0

fracao_frasco_paciente = dose_ui / ui_frasco
custo_toxina_paciente = preco_toxina * fracao_frasco_paciente

custo_insumos_sem_toxina = float(edited["Custo/paciente (R$)"].sum())
custo_base_calculado = custo_insumos_sem_toxina + custo_toxina_paciente
custo_base_total = custo_base_calculado + ajuste_manual

sigma = risk_pct / 100.0
custo_otimista = custo_base_total
custo_realista = custo_base_total * (1 + sigma)
custo_pessimista = custo_base_total * (1 + 2 * sigma)

fee = selling_fees_pct / 100.0
markup = markup_pct / 100.0
friends_markup = friends_markup_pct / 100.0

preco_novos_raw = custo_realista * (1 + markup) / (1 - fee)
preco_amigos_raw = custo_realista * (1 + friends_markup) / (1 - fee)

preco_novos = round_up(preco_novos_raw, float(rounding_step))
preco_amigos = round_up(preco_amigos_raw, float(rounding_step))

taxa_novos = preco_novos * fee
taxa_amigos = preco_amigos * fee

lucro_novos = preco_novos - taxa_novos - custo_realista
lucro_amigos = preco_amigos - taxa_amigos - custo_realista

margem_venda_novos = lucro_novos / preco_novos if preco_novos > 0 else np.nan
margem_venda_amigos = lucro_amigos / preco_amigos if preco_amigos > 0 else np.nan


# =========================================================
# DETALHAMENTO DE CUSTOS
# =========================================================
cost_detail = edited[
    ["Produto", "Custo unitário (R$)", "Qtd/paciente", "Custo/paciente (R$)"]
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

cost_detail = pd.concat([cost_detail, tox_row], ignore_index=True)

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

# Para o donut, a contingência vira um componente explícito.
visual_cost_detail = cost_detail.copy()
risk_value = max(0.0, custo_realista - custo_base_total)
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


# =========================================================
# CENÁRIOS DE PREÇO
# =========================================================
scenario_df = pd.DataFrame(
    {
        "Cenário": ["Otimista", "Realista", "Pessimista"],
        "Custo": [custo_otimista, custo_realista, custo_pessimista],
    }
)
scenario_df["Preço Novos"] = scenario_df["Custo"].apply(
    lambda c: round_up(c * (1 + markup) / (1 - fee), float(rounding_step))
)
scenario_df["Preço Amigos/Família"] = scenario_df["Custo"].apply(
    lambda c: round_up(c * (1 + friends_markup) / (1 - fee), float(rounding_step))
)


# =========================================================
# ESTOQUE E INVESTIMENTO
# =========================================================
capacity_rows = []

for _, row in edited.iterrows():
    qpp = float(row["Qtd/paciente"])

    if qpp > 0:
        qty_available = float(row["Qtd total"])
        if bool(row["Dividido com Julia"]):
            qty_available *= share_carolina_pct / 100.0
        capacity = math.floor(qty_available / qpp)
    else:
        capacity = np.inf

    capacity_rows.append(
        {"Produto": row["Produto"], "Pacientes suportados": capacity}
    )

tox_capacity = (
    math.floor((frascos_disponiveis * ui_frasco) / dose_ui) if dose_ui > 0 else 0
)

capacity_rows.append(
    {
        "Produto": f"Toxina botulínica · {tipo_toxina}",
        "Pacientes suportados": tox_capacity,
    }
)

capacity_df = pd.DataFrame(capacity_rows)
finite_capacity = capacity_df.replace(np.inf, np.nan)["Pacientes suportados"].dropna()
stock_capacity = int(finite_capacity.min()) if not finite_capacity.empty else 0

limiting_items = capacity_df[
    capacity_df["Pacientes suportados"] == stock_capacity
]["Produto"].tolist()

invest_common_full = float(edited["Preço compra (R$)"].sum())
invest_toxin_full = preco_toxina * frascos_disponiveis
invest_total_full = invest_common_full + invest_toxin_full

share = share_carolina_pct / 100.0
carolina_common = float(
    np.where(
        edited["Dividido com Julia"],
        edited["Preço compra (R$)"] * share,
        edited["Preço compra (R$)"],
    ).sum()
)

invest_carolina = carolina_common + invest_toxin_full


# =========================================================
# BREAKEVEN / PROJEÇÃO
# =========================================================
be_operacional = safe_ceil_div(custo_fixo_mensal, lucro_novos)
parcela_investimento = invest_carolina / meses_payback
be_payback = safe_ceil_div(custo_fixo_mensal + parcela_investimento, lucro_novos)
be_caixa_bruto = safe_ceil_div(invest_carolina, preco_novos)

receita_mes = pacientes_mes * preco_novos
taxas_mes = receita_mes * fee
custo_variavel_mes = pacientes_mes * custo_realista
contribuicao_mes = receita_mes - taxas_mes - custo_variavel_mes
resultado_operacional_mes = contribuicao_mes - custo_fixo_mensal
resultado_apos_payback = resultado_operacional_mes - parcela_investimento

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


# =========================================================
# ABA 1 — SAÍDAS
# =========================================================
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
        '<div class="kpi-badges">'
        + margin_badge
        + f'<span class="badge badge-neutral">Frasco ativo: {tipo_toxina}</span>'
        + f'<span class="badge badge-neutral">{dose_ui:.0f} UI / paciente</span>'
        + "</div>",
        unsafe_allow_html=True,
    )

with tab1_charts:
    st.markdown("#### Leitura visual")
    st.markdown(
        '<div class="visual-version-note">'
        'Nova visualização: rosca com percentuais sempre visíveis + barras sem navegação e com animação de subida/descida.'
        '</div>',
        unsafe_allow_html=True,
    )
    ch1, ch2 = st.columns([1.05, 1.15])

    with ch1:
        st.markdown(
            donut_html(visual_cost_detail, custo_realista),
            unsafe_allow_html=True,
        )

    with ch2:
        animated_scenario_bars(scenario_df)

with tab1_insights:
    if dose_ui != 50:
        st.warning(
            "A premissa principal informada é 50 UI por aplicação. "
            "Esta simulação está usando outra dose."
        )

    st.markdown(
        f"""
        <div class="soft-panel">
            <b>Leitura rápida:</b> com o frasco de <b>{tipo_toxina}</b>,
            a toxina representa <b>{brl(custo_toxina_paciente)}</b> por aplicação.
            No cenário realista, o procedimento custa <b>{brl(custo_realista)}</b>
            e gera aproximadamente <span class="positive">{brl(lucro_novos)}</span>
            de contribuição por paciente novo.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# ABA 2 — SAÍDAS
# =========================================================
with tab2_outputs:
    st.markdown("#### Custo calculado por item")
    st.caption(
        "Tabela de leitura: os valores abaixo são calculados automaticamente e não são editáveis."
    )

    calc_toolbar1, calc_toolbar2, calc_toolbar3 = st.columns([1.25, 1.1, 4.65])
    with calc_toolbar1:
        st.button(
            "↺ Restaurar custos originais",
            on_click=reset_insumos,
            key="reset_insumos_calc",
            use_container_width=True,
        )
    with calc_toolbar2:
        history_count_calc = len(st.session_state.get("insumos_history", []))
        st.button(
            f"↶ Desfazer ({history_count_calc}/10)",
            on_click=undo_insumo_action,
            key="undo_insumos_calc",
            use_container_width=True,
            disabled=history_count_calc == 0,
        )
    with calc_toolbar3:
        st.markdown(
            '<span class="badge badge-neutral">Somente leitura</span>'
            '<span class="badge badge-green">Atualização automática</span>',
            unsafe_allow_html=True,
        )

    st.markdown(calculated_table_html(cost_detail), unsafe_allow_html=True)

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
        st.caption("Gargalo atual de estoque: " + ", ".join(limiting_items))

    with st.expander("Ver capacidade estimada de cada item"):
        cap_rows = []
        for _, row in capacity_df.iterrows():
            supported = (
                "∞"
                if row["Pacientes suportados"] == np.inf
                else str(int(row["Pacientes suportados"]))
            )
            cap_rows.append(
                f"""
                <tr>
                    <td class="product">{html.escape(str(row["Produto"]))}</td>
                    <td class="money">{supported}</td>
                </tr>
                """
            )
        st.markdown(
            f"""
            <div class="calc-table-wrap">
                <table class="calc-table">
                    <thead>
                        <tr>
                            <th>Produto</th>
                            <th style="text-align:right">Pacientes suportados</th>
                        </tr>
                    </thead>
                    <tbody>{''.join(cap_rows)}</tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# ABA 3 — SAÍDAS
# =========================================================
with tab3_outputs:
    st.markdown("#### Indicadores de sustentabilidade")

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        kpi_card(
            "Investimento inicial",
            brl(invest_carolina),
            "Desembolso estimado da Dra. Carolina considerando itens compartilhados.",
        )

    with d2:
        kpi_card(
            "Breakeven operacional",
            f"{be_operacional} pac./mês" if be_operacional is not None else "—",
            "Volume necessário para cobrir os custos fixos mensais.",
        )

    with d3:
        kpi_card(
            f"BE + payback em {meses_payback} mês(es)",
            f"{be_payback} pac./mês" if be_payback is not None else "—",
            "Cobre fixos e recupera o investimento no prazo-alvo.",
            variant="highlight",
        )

    with d4:
        kpi_card(
            "Resultado mensal",
            brl(resultado_operacional_mes),
            f"Com a simulação de {pacientes_mes} pacientes/mês.",
            variant="profit" if resultado_operacional_mes >= 0 else "default",
        )

    st.markdown("#### Projeção do mês")
    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.metric("Receita projetada", brl(receita_mes))
    with q2:
        st.metric("Custo variável", brl(custo_variavel_mes))
    with q3:
        st.metric(
            "Payback estimado",
            f"{payback_estimado:.1f} meses" if np.isfinite(payback_estimado) else "—",
        )
    with q4:
        st.metric(
            "ROI mensal estimado",
            pct(roi_mensal) if np.isfinite(roi_mensal) else "—",
        )

    max_patients_chart = max(30, int(pacientes_mes * 2), (be_payback or 0) + 10)
    patients = np.arange(0, max_patients_chart + 1)

    profit_curve = (
        patients * preco_novos * (1 - fee)
        - patients * custo_realista
        - custo_fixo_mensal
        - parcela_investimento
    )

    fig_be = go.Figure()
    fig_be.add_trace(
        go.Scatter(
            x=patients,
            y=profit_curve,
            mode="lines",
            line=dict(color=ROSE_DARK, width=3),
            fill="tozeroy",
            fillcolor="rgba(185, 134, 124, 0.10)",
            hovertemplate="%{x} pacientes<br>R$ %{y:,.2f}<extra></extra>",
            name="Resultado",
        )
    )
    fig_be.add_hline(
        y=0,
        line_dash="dash",
        line_color="#9D9691",
        annotation_text="Equilíbrio",
        annotation_font_color=TEXT,
    )

    if be_payback is not None:
        fig_be.add_vline(
            x=be_payback,
            line_dash="dot",
            line_color=GOLD,
            annotation_text=f"BE: {be_payback} pac.",
            annotation_font_color=TEXT,
        )

    fig_be.update_layout(
        title="Resultado mensal conforme o número de pacientes",
        height=430,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color=TEXT),
        title_font=dict(color=TEXT),
        xaxis_title="Pacientes por mês",
        yaxis_title="Resultado (R$)",
        showlegend=False,
        dragmode=False,
        hovermode="x unified",
    )
    fig_be.update_yaxes(gridcolor="#EEE8E4", fixedrange=True, color=TEXT)
    fig_be.update_xaxes(gridcolor="#F3EFEC", fixedrange=True, color=TEXT)

    st.plotly_chart(fig_be, use_container_width=True, config=PLOT_CONFIG)

    if resultado_operacional_mes >= meta_resultado_mensal and meta_resultado_mensal > 0:
        st.success(
            f"Meta atingida: a simulação supera {brl(meta_resultado_mensal)} "
            f"de resultado mensal."
        )

        if not st.session_state.get("meta_celebrada", False):
            st.balloons()
            st.session_state["meta_celebrada"] = True
    else:
        st.session_state["meta_celebrada"] = False

    with st.expander("Entender os três pontos de equilíbrio"):
        st.markdown(
            f"""
            **Breakeven operacional:** {be_operacional if be_operacional is not None else "—"} pacientes/mês  
            Cobre os custos fixos mensais usando a contribuição de cada procedimento.

            **Breakeven com payback:** {be_payback if be_payback is not None else "—"} pacientes/mês  
            Além dos custos fixos, recupera o desembolso inicial em {meses_payback} mês(es).

            **Recuperação simples de caixa:** {be_caixa_bruto if be_caixa_bruto is not None else "—"} pacientes  
            Leitura simplificada do investimento inicial dividido pela receita bruta por procedimento.
            """
        )


# =========================================================
# ABA 4 — COMPARATIVO DOS FRASCOS
# =========================================================
comparison = pd.DataFrame(
    [
        {
            "Frasco": "100 UI",
            "Preço do frasco": preco_toxina_100,
            "Custo por UI": preco_toxina_100 / 100.0 if preco_toxina_100 > 0 else 0,
            "Custo toxina/paciente": preco_toxina_100 * dose_ui / 100.0,
            "Pacientes teóricos/frasco": math.floor(100.0 / dose_ui) if dose_ui > 0 else 0,
        },
        {
            "Frasco": "200 UI",
            "Preço do frasco": preco_toxina_200,
            "Custo por UI": preco_toxina_200 / 200.0 if preco_toxina_200 > 0 else 0,
            "Custo toxina/paciente": preco_toxina_200 * dose_ui / 200.0,
            "Pacientes teóricos/frasco": math.floor(200.0 / dose_ui) if dose_ui > 0 else 0,
        },
    ]
)
comparison["Ativo no cálculo"] = comparison["Frasco"].eq(tipo_toxina)

with tab4_outputs:
    best_idx = comparison["Custo toxina/paciente"].idxmin()
    best_row = comparison.loc[best_idx]

    a, b, c = st.columns(3)

    with a:
        kpi_card(
            "100 UI · custo/paciente",
            brl(comparison.loc[0, "Custo toxina/paciente"]),
            f"{comparison.loc[0, 'Pacientes teóricos/frasco']} pacientes teóricos por frasco.",
        )

    with b:
        kpi_card(
            "200 UI · custo/paciente",
            brl(comparison.loc[1, "Custo toxina/paciente"]),
            f"{comparison.loc[1, 'Pacientes teóricos/frasco']} pacientes teóricos por frasco.",
        )

    with c:
        economia = abs(
            comparison.loc[0, "Custo toxina/paciente"]
            - comparison.loc[1, "Custo toxina/paciente"]
        )
        kpi_card(
            "Melhor custo teórico",
            str(best_row["Frasco"]),
            f"Economia de {brl(economia)} por paciente vs. a outra opção.",
            variant="profit",
        )

    st.markdown("#### Comparação visual")
    animated_two_bars(
        labels=["100 UI", "200 UI"],
        values=[
            float(comparison.loc[0, "Custo toxina/paciente"]),
            float(comparison.loc[1, "Custo toxina/paciente"]),
        ],
        colors=[ROSE_DARK, GOLD],
        title=f"Custo da toxina para uma aplicação de {dose_ui:.0f} UI",
        subtitle="Sem navegação no gráfico · valores visíveis e barras animadas a cada alteração.",
        state_key="prev_flask_chart",
    )

    comparison_rows = []
    for _, row in comparison.iterrows():
        comparison_rows.append(
            f"""
            <tr>
                <td class="product">{html.escape(str(row["Frasco"]))}</td>
                <td class="money">{brl(float(row["Preço do frasco"]))}</td>
                <td class="money">{brl(float(row["Custo por UI"]))}</td>
                <td class="money">{brl(float(row["Custo toxina/paciente"]))}</td>
                <td class="qty">{int(row["Pacientes teóricos/frasco"])}</td>
                <td>{'Sim' if bool(row["Ativo no cálculo"]) else 'Não'}</td>
            </tr>
            """
        )

    st.markdown(
        f"""
        <div class="calc-table-wrap">
            <table class="calc-table">
                <thead>
                    <tr>
                        <th>Frasco</th>
                        <th style="text-align:right">Preço</th>
                        <th style="text-align:right">Custo/UI</th>
                        <th style="text-align:right">Custo/paciente</th>
                        <th style="text-align:right">Pacientes/frasco</th>
                        <th>Ativo</th>
                    </tr>
                </thead>
                <tbody>{''.join(comparison_rows)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="soft-panel">
            Com os preços atuais, o frasco de <b>{best_row["Frasco"]}</b>
            apresenta o menor custo teórico de toxina por paciente:
            <span class="positive">{brl(best_row["Custo toxina/paciente"])}</span>.
            A decisão final também deve considerar o aproveitamento real do frasco
            e a programação de pacientes.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# EXPORTAÇÃO DISCRETA
# =========================================================
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
        ["Capacidade estimada do estoque", stock_capacity],
        ["Breakeven operacional", be_operacional],
        ["Breakeven com payback", be_payback],
        ["Pacientes projetados por mês", pacientes_mes],
        ["Resultado operacional mensal", resultado_operacional_mes],
    ],
    columns=["Indicador", "Valor"],
)

csv = summary_export.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")

st.divider()

with st.expander("⬇️ Exportar resumo", expanded=False):
    st.caption("Baixe os principais números da simulação atual em CSV.")
    st.download_button(
        "Baixar resumo financeiro",
        data=csv,
        file_name="resumo_financeiro_botox.csv",
        mime="text/csv",
        use_container_width=False,
    )

st.caption(
    "Modelo financeiro gerencial. Antes de definir o preço final, valide custos tributários, "
    "política de retoques, desperdício real, taxas e demais despesas da operação."
)
