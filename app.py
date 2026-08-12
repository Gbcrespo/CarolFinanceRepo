import math
from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# CONFIGURAÇÃO GERAL
# =========================================================
st.set_page_config(
    page_title="Planejamento Financeiro | Dra. Carolina Bittencourt",
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

# =========================================================
# CSS CUSTOMIZADO — VISUAL EXECUTIVO / SaaS
# =========================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background: {BG};
            color: {TEXT};
        }}

        .block-container {{
            max-width: 1480px;
            padding-top: 1.7rem;
            padding-bottom: 2.5rem;
        }}

        h1, h2, h3, h4 {{
            color: {TEXT};
            letter-spacing: -0.02em;
        }}

        p, label, .stMarkdown {{
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
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid #EEE8E4;
            border-radius: 16px;
            padding: 18px 20px;
            margin: 4px 0 14px 0;
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            border-radius: 10px 10px 0 0;
            padding-left: 16px;
            padding-right: 16px;
            font-weight: 650;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            background: #F3E9E5;
            color: #8E625A;
        }}

        div[data-baseweb="tab-border"] {{
            background-color: #E8DDD7;
        }}

        /* Inputs */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            border-radius: 10px !important;
        }}

        div[data-testid="stNumberInput"] input {{
            border-radius: 10px;
        }}

        /* Data editor */
        div[data-testid="stDataFrame"] {{
            border: 1px solid #ECE7E3;
            border-radius: 14px;
            overflow: hidden;
        }}

        /* Expander */
        details {{
            background: rgba(255,255,255,0.60);
            border: 1px solid #EEE8E4 !important;
            border-radius: 12px !important;
        }}

        /* Download */
        .stDownloadButton > button {{
            border-radius: 10px;
            border: 1px solid #D9CCC4;
            background: #FFFDFB;
            color: {TEXT};
        }}

        /* Divisores mais suaves */
        hr {{
            border-color: #EEE8E4;
        }}

        /* Oculta elementos de interface menos úteis */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        @media (max-width: 900px) {{
            .hero-title {{
                font-size: 1.55rem;
            }}
            .kpi-card {{
                min-height: 125px;
                margin-bottom: 8px;
            }}
        }}
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


# =========================================================
# HELPERS
# =========================================================
def brl(value: float) -> str:
    """Formata número como R$ sem depender do locale do sistema."""
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


def kpi_card(
    label: str,
    value: str,
    subtitle: str,
    variant: str = "default",
) -> None:
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


# =========================================================
# CABEÇALHO
# =========================================================
st.markdown(
    """
    <div class="hero">
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
# ABA 1 — INPUTS RÁPIDOS + PLACEHOLDERS DE SAÍDA
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
            help=(
                "O percentual é aplicado sobre o custo. Ex.: 150% de markup "
                "significa preço = 2,5 × custo."
            ),
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
                help="Use para descarte, retoques previstos, deslocamento ou itens não listados.",
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

    # Saídas serão preenchidas após todos os inputs das demais abas serem lidos.
    tab1_kpis = st.container()
    tab1_charts = st.container()
    tab1_insights = st.container()


# =========================================================
# ABA 2 — EDITOR DE INSUMOS
# =========================================================
with tabs[1]:
    section_intro(
        "Insumos e custos",
        "Edite apenas o que mudou. A tabela recalcula automaticamente o custo unitário e o custo por paciente.",
    )

    edited = st.data_editor(
        DEFAULT_INPUTS,
        key="insumos_editor",
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        column_config={
            "Produto": st.column_config.TextColumn("Produto", disabled=True),
            "Preço compra (R$)": st.column_config.NumberColumn(
                "Preço de compra",
                min_value=0.0,
                step=0.01,
                format="R$ %.2f",
                help="Valor total pago pela embalagem, caixa ou frasco.",
            ),
            "Qtd total": st.column_config.NumberColumn(
                "Quantidade total",
                min_value=0.0001,
                step=1.0,
                format="%.2f",
                help="Quantidade contida na compra.",
            ),
            "Unidade": st.column_config.TextColumn("Unidade", disabled=True),
            "Qtd/paciente": st.column_config.NumberColumn(
                "Uso por paciente",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                help="Quantidade média utilizada em cada procedimento.",
            ),
            "Dividido com Julia": st.column_config.CheckboxColumn(
                "Dividido com Julia",
                help="Afeta o desembolso inicial da Dra. Carolina.",
            ),
        },
    )

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
# ABA 3 — INPUTS AVANÇADOS + PLACEHOLDERS
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
            help="Sala, marketing, software, contabilidade, secretária etc.",
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
            help="Em quantos meses você gostaria de recuperar o desembolso inicial.",
        )
    with p4:
        meta_resultado_mensal = st.number_input(
            "Meta de resultado mensal (R$)",
            min_value=0.0,
            value=3000.0,
            step=250.0,
            format="%.2f",
            key="meta_resultado_mensal",
            help="Ao atingir a meta na simulação, o dashboard comemora com uma microanimação.",
        )

    tab3_outputs = st.container()


# =========================================================
# ABA 4 — PREÇOS DE FRASCOS + PLACEHOLDERS
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
# SANITIZAÇÃO DOS DADOS
# =========================================================
edited = edited.copy()

for col in ["Preço compra (R$)", "Qtd total", "Qtd/paciente"]:
    edited[col] = pd.to_numeric(edited[col], errors="coerce").fillna(0.0)

edited["Dividido com Julia"] = edited["Dividido com Julia"].fillna(False).astype(bool)

if (edited["Qtd total"] <= 0).any():
    st.error("A quantidade total de todos os insumos deve ser maior que zero.")
    st.stop()

if dose_ui != 50:
    with tab1_insights:
        st.warning("A premissa principal informada é 50 UI por aplicação. Esta simulação está usando outra dose.")


# =========================================================
# CÁLCULOS CENTRAIS
# =========================================================
edited["Custo unitário (R$)"] = (
    edited["Preço compra (R$)"] / edited["Qtd total"]
)
edited["Custo/paciente (R$)"] = (
    edited["Custo unitário (R$)"] * edited["Qtd/paciente"]
)

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
        {
            "Produto": row["Produto"],
            "Pacientes suportados": capacity,
        }
    )

tox_capacity = (
    math.floor((frascos_disponiveis * ui_frasco) / dose_ui)
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
be_payback = safe_ceil_div(
    custo_fixo_mensal + parcela_investimento,
    lucro_novos,
)

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
        margin_badge
        + f'<span class="badge badge-neutral">Frasco ativo: {tipo_toxina}</span>'
        + f'<span class="badge badge-neutral">{dose_ui:.0f} UI / paciente</span>',
        unsafe_allow_html=True,
    )

with tab1_charts:
    st.markdown("#### Leitura visual")
    ch1, ch2 = st.columns([1, 1.25])

    with ch1:
        pie_df = cost_detail[cost_detail["Custo/paciente (R$)"] > 0].copy()

        fig_pie = go.Figure(
            data=[
                go.Pie(
                    labels=pie_df["Produto"],
                    values=pie_df["Custo/paciente (R$)"],
                    hole=0.64,
                    textinfo="percent",
                    hovertemplate="<b>%{label}</b><br>R$ %{value:.2f}<br>%{percent}<extra></extra>",
                    marker=dict(
                        colors=[
                            ROSE_DARK,
                            ROSE,
                            GOLD,
                            "#D5B9AE",
                            "#B7C9BE",
                            "#D9C9B8",
                            "#C9C4C0",
                            "#E5D5C9",
                            "#A7B9AE",
                            "#DCC5C0",
                            "#CFB073",
                            "#D8DDD9",
                        ]
                    ),
                )
            ]
        )

        fig_pie.add_annotation(
            text=f"<b>{brl(custo_realista)}</b><br><span style='font-size:11px'>custo realista</span>",
            x=0.5,
            y=0.5,
            font=dict(size=14, color=TEXT),
            showarrow=False,
        )

        fig_pie.update_layout(
            title="Composição do custo",
            height=390,
            margin=dict(l=10, r=10, t=55, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            showlegend=False,
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    with ch2:
        bar_df = scenario_df.melt(
            id_vars="Cenário",
            value_vars=["Custo", "Preço Novos", "Preço Amigos/Família"],
            var_name="Indicador",
            value_name="Valor",
        )

        fig_bar = px.bar(
            bar_df,
            x="Cenário",
            y="Valor",
            color="Indicador",
            barmode="group",
            color_discrete_map={
                "Custo": "#CFC7C2",
                "Preço Novos": ROSE_DARK,
                "Preço Amigos/Família": GOLD,
            },
        )

        fig_bar.update_traces(
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>"
        )

        fig_bar.update_layout(
            title="Precificação por cenário",
            height=390,
            margin=dict(l=10, r=10, t=55, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            legend_title_text="",
            yaxis_title="R$",
            xaxis_title="",
        )

        fig_bar.update_yaxes(gridcolor="#EEE8E4")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab1_insights:
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

    detail_display = cost_detail.copy()
    detail_display["Custo unitário"] = detail_display["Custo unitário (R$)"].map(brl)
    detail_display["Custo por paciente"] = detail_display["Custo/paciente (R$)"].map(brl)

    st.dataframe(
        detail_display[
            ["Produto", "Custo unitário", "Qtd/paciente", "Custo por paciente"]
        ],
        use_container_width=True,
        hide_index=True,
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
        st.caption("Gargalo atual de estoque: " + ", ".join(limiting_items))

    with st.expander("Ver capacidade estimada de cada item"):
        capacity_show = capacity_df.copy()
        capacity_show["Pacientes suportados"] = capacity_show[
            "Pacientes suportados"
        ].apply(lambda x: "∞" if x == np.inf else int(x))
        st.dataframe(capacity_show, use_container_width=True, hide_index=True)


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

    max_patients_chart = max(
        30,
        int(pacientes_mes * 2),
        (be_payback or 0) + 10,
    )

    patients = np.arange(0, max_patients_chart + 1)

    profit_curve = (
        patients * preco_novos * (1 - fee)
        - patients * custo_realista
        - custo_fixo_mensal
        - parcela_investimento
    )

    be_curve_df = pd.DataFrame(
        {
            "Pacientes/mês": patients,
            "Resultado após custos + payback (R$)": profit_curve,
        }
    )

    fig_be = go.Figure()

    fig_be.add_trace(
        go.Scatter(
            x=be_curve_df["Pacientes/mês"],
            y=be_curve_df["Resultado após custos + payback (R$)"],
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
    )

    if be_payback is not None:
        fig_be.add_vline(
            x=be_payback,
            line_dash="dot",
            line_color=GOLD,
            annotation_text=f"BE: {be_payback} pac.",
        )

    fig_be.update_layout(
        title="Resultado mensal conforme o número de pacientes",
        height=430,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
        xaxis_title="Pacientes por mês",
        yaxis_title="Resultado (R$)",
        showlegend=False,
    )

    fig_be.update_yaxes(gridcolor="#EEE8E4")
    fig_be.update_xaxes(gridcolor="#F3EFEC")

    st.plotly_chart(fig_be, use_container_width=True)

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

    fig_compare = px.bar(
        comparison,
        x="Frasco",
        y="Custo toxina/paciente",
        text="Custo toxina/paciente",
        color="Frasco",
        color_discrete_map={
            "100 UI": ROSE_DARK,
            "200 UI": GOLD,
        },
    )

    fig_compare.update_traces(
        texttemplate="R$ %{text:.2f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>R$ %{y:.2f} / paciente<extra></extra>",
    )

    fig_compare.update_layout(
        title=f"Custo da toxina para uma aplicação de {dose_ui:.0f} UI",
        height=390,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis_title="",
        yaxis_title="R$ por paciente",
    )

    fig_compare.update_yaxes(gridcolor="#EEE8E4")
    st.plotly_chart(fig_compare, use_container_width=True)

    comparison_display = comparison.copy()
    comparison_display["Preço do frasco"] = comparison_display["Preço do frasco"].map(brl)
    comparison_display["Custo por UI"] = comparison_display["Custo por UI"].map(brl)
    comparison_display["Custo toxina/paciente"] = comparison_display[
        "Custo toxina/paciente"
    ].map(brl)
    comparison_display["Ativo no cálculo"] = comparison_display[
        "Ativo no cálculo"
    ].map({True: "Sim", False: "Não"})

    st.dataframe(
        comparison_display,
        use_container_width=True,
        hide_index=True,
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
