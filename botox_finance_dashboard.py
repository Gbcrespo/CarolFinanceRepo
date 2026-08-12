import math
from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Planejamento Financeiro | Botox - Dra. Carolina Bittencourt",
    page_icon="💉",
    layout="wide",
)


# -----------------------------
# Dados-base da planilha enviada
# -----------------------------
DEFAULT_INPUTS = pd.DataFrame(
    [
        {
            "Produto": "Clorexidina 100 ml",
            "Preço compra (R$)": 12.99,
            "Qtd total": 1.0,
            "Unidade": "frasco",
            "Qtd/paciente": 0.10,
            "Dividido com Julia": False,
        },
        {
            "Produto": "Gaze",
            "Preço compra (R$)": 15.48,
            "Qtd total": 1.0,
            "Unidade": "caixa",
            "Qtd/paciente": 0.20,
            "Dividido com Julia": False,
        },
        {
            "Produto": "Seringas 50 UI",
            "Preço compra (R$)": 84.00,
            "Qtd total": 50.0,
            "Unidade": "unidades",
            "Qtd/paciente": 2.00,
            "Dividido com Julia": True,
        },
        {
            "Produto": "Seringas de 1 ml",
            "Preço compra (R$)": 20.00,
            "Qtd total": 50.0,
            "Unidade": "unidades",
            "Qtd/paciente": 1.00,
            "Dividido com Julia": True,
        },
        {
            "Produto": "Salina estéril frasquinhos",
            "Preço compra (R$)": 18.25,
            "Qtd total": 25.0,
            "Unidade": "unidades",
            "Qtd/paciente": 1.00,
            "Dividido com Julia": True,
        },
        {
            "Produto": "Luvas",
            "Preço compra (R$)": 28.00,
            "Qtd total": 100.0,
            "Unidade": "unidades",
            "Qtd/paciente": 2.00,
            "Dividido com Julia": False,
        },
        {
            "Produto": "Anestésico",
            "Preço compra (R$)": 93.00,
            "Qtd total": 1.0,
            "Unidade": "frasco",
            "Qtd/paciente": 0.05,
            "Dividido com Julia": False,
        },
        {
            "Produto": "Sabonete",
            "Preço compra (R$)": 5.00,
            "Qtd total": 1.0,
            "Unidade": "unidade",
            "Qtd/paciente": 0.10,
            "Dividido com Julia": False,
        },
        {
            "Produto": "Lápis marcador branco",
            "Preço compra (R$)": 15.00,
            "Qtd total": 1.0,
            "Unidade": "unidade",
            "Qtd/paciente": 0.05,
            "Dividido com Julia": False,
        },
        {
            "Produto": "Faixas pro cabelo",
            "Preço compra (R$)": 15.00,
            "Qtd total": 20.0,
            "Unidade": "unidades",
            "Qtd/paciente": 1.00,
            "Dividido com Julia": False,
        },
    ]
)


def brl(value: float) -> str:
    """Formata número como moeda brasileira sem depender de locale do SO."""
    if value is None or not np.isfinite(value):
        return "—"
    s = f"{value:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
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


# -----------------------------
# Cabeçalho
# -----------------------------
st.title("Planejamento Financeiro — Aplicação de Botox")
st.caption(
    "Dra. Carolina Bittencourt | Custos, risco, precificação, estoque e breakeven em tempo real"
)

with st.expander("Como o modelo funciona", expanded=False):
    st.markdown(
        """
- O custo unitário de cada insumo é **Preço de compra ÷ Quantidade total**.
- O custo por paciente é **custo unitário × quantidade usada por paciente**.
- A toxina é tratada separadamente: é possível selecionar **frasco de 100 UI OU 200 UI**, nunca os dois simultaneamente no procedimento.
- A dose padrão foi configurada em **50 UI por paciente**, conforme a premissa informada. O campo permanece editável apenas para análises de sensibilidade.
- O risco é modelado em três cenários: **otimista = custo base**, **realista = base + 1σ** e **pessimista = base + 2σ**, onde σ é o percentual de contingência escolhido.
- O controle de “margem” de 50% a 300% é tratado tecnicamente como **markup sobre o custo**, pois margem bruta, em sentido financeiro, não pode superar 100%.
        """
    )


# -----------------------------
# Painel lateral: parâmetros
# -----------------------------
with st.sidebar:
    st.header("Parâmetros do modelo")

    st.subheader("Toxina")
    tipo_toxina = st.radio(
        "Frasco utilizado",
        options=["100 UI", "200 UI"],
        horizontal=True,
        help="Somente a opção selecionada entra no custo, estoque e investimento.",
    )

    preco_toxina_100 = st.number_input(
        "Preço do frasco 100 UI (R$)",
        min_value=0.0,
        value=575.0,
        step=5.0,
        format="%.2f",
    )
    preco_toxina_200 = st.number_input(
        "Preço do frasco 200 UI (R$)",
        min_value=0.0,
        value=1000.0,
        step=5.0,
        format="%.2f",
    )
    frascos_toxina = st.number_input(
        "Frascos comprados/disponíveis",
        min_value=0,
        value=1,
        step=1,
    )
    dose_ui = st.number_input(
        "Dose utilizada por paciente (UI)",
        min_value=1.0,
        max_value=400.0,
        value=50.0,
        step=1.0,
        help="Premissa padrão: 50 UI. Edite apenas para simulações.",
    )
    if dose_ui != 50:
        st.warning("A premissa principal informada é 50 UI por aplicação.")

    st.divider()
    st.subheader("Preço e risco")
    markup_pct = st.slider(
        "Markup desejado sobre o custo (%)",
        min_value=50,
        max_value=300,
        value=150,
        step=5,
    )
    risk_pct = st.slider(
        "Risco / contingência (σ)",
        min_value=0,
        max_value=30,
        value=10,
        step=1,
        format="%d%%",
    )
    friends_markup_pct = st.slider(
        "Markup Amigos/Familiares (%)",
        min_value=10,
        max_value=100,
        value=40,
        step=5,
        help="Markup reduzido, porém sempre positivo sobre o custo realista.",
    )
    selling_fees_pct = st.slider(
        "Taxas/impostos sobre a venda (%)",
        min_value=0.0,
        max_value=30.0,
        value=0.0,
        step=0.5,
        help="Ex.: taxa de cartão, impostos ou comissão proporcional ao preço.",
    )
    rounding_step = st.selectbox(
        "Arredondar preços sugeridos para",
        options=[1, 5, 10, 25, 50],
        index=2,
        format_func=lambda x: f"R$ {x}",
    )

    st.divider()
    st.subheader("Ajustes operacionais")
    ajuste_manual = st.number_input(
        "Adicionais manuais por paciente (R$)",
        min_value=0.0,
        value=0.0,
        step=5.0,
        format="%.2f",
        help="Inclua itens não listados, deslocamento, descarte, retoque previsto etc.",
    )
    custo_fixo_mensal = st.number_input(
        "Custos fixos mensais (R$)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        format="%.2f",
        help="Ex.: sala, secretária, software, marketing, contabilidade.",
    )
    pacientes_mes = st.number_input(
        "Pacientes esperados por mês",
        min_value=0,
        value=10,
        step=1,
    )
    meses_payback = st.number_input(
        "Prazo-alvo para recuperar investimento (meses)",
        min_value=1,
        max_value=36,
        value=3,
        step=1,
    )

    st.divider()
    st.subheader("Itens divididos com Julia")
    share_carolina_pct = st.slider(
        "Parcela paga pela Dra. Carolina (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help=(
            "Afeta o desembolso inicial da Dra. Carolina. "
            "O custo econômico por paciente permanece pelo custo unitário integral."
        ),
    )


# -----------------------------
# Editor de insumos
# -----------------------------
st.subheader("1) Insumos editáveis")
st.write(
    "Edite preços, quantidades disponíveis e consumo por paciente. "
    "Todos os cálculos abaixo são atualizados automaticamente."
)

edited = st.data_editor(
    DEFAULT_INPUTS,
    key="insumos_editor",
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic",
    column_config={
        "Produto": st.column_config.TextColumn("Produto", required=True),
        "Preço compra (R$)": st.column_config.NumberColumn(
            "Preço compra (R$)", min_value=0.0, step=0.01, format="R$ %.2f"
        ),
        "Qtd total": st.column_config.NumberColumn(
            "Qtd total", min_value=0.0001, step=1.0, format="%.2f"
        ),
        "Unidade": st.column_config.TextColumn("Unidade"),
        "Qtd/paciente": st.column_config.NumberColumn(
            "Qtd/paciente", min_value=0.0, step=0.01, format="%.2f"
        ),
        "Dividido com Julia": st.column_config.CheckboxColumn("Dividido com Julia"),
    },
)

edited = edited.copy()
for col in ["Preço compra (R$)", "Qtd total", "Qtd/paciente"]:
    edited[col] = pd.to_numeric(edited[col], errors="coerce").fillna(0.0)

if (edited["Qtd total"] <= 0).any():
    st.error("Todas as quantidades totais devem ser maiores que zero.")
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

# Cenários de risco
sigma = risk_pct / 100.0
custo_otimista = custo_base_total
custo_realista = custo_base_total * (1 + sigma)
custo_pessimista = custo_base_total * (1 + 2 * sigma)

# Precificação com proteção contra taxas percentuais sobre venda
fee = selling_fees_pct / 100.0
if fee >= 1:
    st.error("Taxas/impostos sobre venda devem ser inferiores a 100%.")
    st.stop()

markup = markup_pct / 100.0
friends_markup = friends_markup_pct / 100.0

preco_novos_raw = custo_realista * (1 + markup) / (1 - fee)
preco_amigos_raw = custo_realista * (1 + friends_markup) / (1 - fee)

preco_novos = round_up(preco_novos_raw, float(rounding_step))
preco_amigos = round_up(preco_amigos_raw, float(rounding_step))

taxa_novos = preco_novos * fee
taxa_amigos = preco_amigos * fee

contrib_novos = preco_novos - taxa_novos - custo_realista
contrib_amigos = preco_amigos - taxa_amigos - custo_realista

margem_bruta_novos = contrib_novos / preco_novos if preco_novos > 0 else np.nan
margem_bruta_amigos = contrib_amigos / preco_amigos if preco_amigos > 0 else np.nan


# -----------------------------
# KPIs principais
# -----------------------------
st.subheader("2) Resumo financeiro por paciente")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Custo base direto", brl(custo_base_calculado))
k2.metric("Custo + adicionais", brl(custo_base_total))
k3.metric("Custo realista (+1σ)", brl(custo_realista))
k4.metric("Preço sugerido — novos", brl(preco_novos))
k5.metric("Preço — amigos/família", brl(preco_amigos))

st.caption(
    f"Frasco ativo: {tipo_toxina} | Dose: {dose_ui:.0f} UI | "
    f"Fração de frasco por paciente: {fracao_frasco_paciente:.2f} | "
    f"Custo de toxina/paciente: {brl(custo_toxina_paciente)}"
)


# -----------------------------
# Composição de custos
# -----------------------------
cost_detail = edited[
    ["Produto", "Custo unitário (R$)", "Qtd/paciente", "Custo/paciente (R$)"]
].copy()

tox_row = pd.DataFrame(
    [
        {
            "Produto": f"Toxina botulínica — {tipo_toxina}",
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
                        "Produto": "Ajustes/adicionais manuais",
                        "Custo unitário (R$)": ajuste_manual,
                        "Qtd/paciente": 1.0,
                        "Custo/paciente (R$)": ajuste_manual,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

left, right = st.columns([1.25, 1])

with left:
    st.markdown("#### Composição do custo")
    display_cost_detail = cost_detail.copy()
    display_cost_detail["Custo unitário"] = display_cost_detail["Custo unitário (R$)"].map(brl)
    display_cost_detail["Custo por paciente"] = display_cost_detail["Custo/paciente (R$)"].map(brl)
    st.dataframe(
        display_cost_detail[
            ["Produto", "Custo unitário", "Qtd/paciente", "Custo por paciente"]
        ],
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.markdown("#### Participação no custo por paciente")
    pie_df = cost_detail[cost_detail["Custo/paciente (R$)"] > 0].copy()
    fig_pie = px.pie(
        pie_df,
        names="Produto",
        values="Custo/paciente (R$)",
        hole=0.45,
    )
    fig_pie.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_pie, use_container_width=True)


# -----------------------------
# Cenários e precificação
# -----------------------------
st.subheader("3) Cenários de risco e precificação")

scenario_df = pd.DataFrame(
    {
        "Cenário": ["Otimista (uso exato)", "Realista (+1σ)", "Pessimista (+2σ)"],
        "Custo por paciente (R$)": [
            custo_otimista,
            custo_realista,
            custo_pessimista,
        ],
    }
)
scenario_df["Preço novos (R$)"] = scenario_df["Custo por paciente (R$)"].apply(
    lambda c: round_up(c * (1 + markup) / (1 - fee), float(rounding_step))
)
scenario_df["Preço amigos/família (R$)"] = scenario_df["Custo por paciente (R$)"].apply(
    lambda c: round_up(c * (1 + friends_markup) / (1 - fee), float(rounding_step))
)
scenario_df["Lucro/contribuição novos (R$)"] = (
    scenario_df["Preço novos (R$)"] * (1 - fee)
    - scenario_df["Custo por paciente (R$)"]
)

scenario_display = scenario_df.copy()
for c in [
    "Custo por paciente (R$)",
    "Preço novos (R$)",
    "Preço amigos/família (R$)",
    "Lucro/contribuição novos (R$)",
]:
    scenario_display[c] = scenario_display[c].map(brl)

st.dataframe(scenario_display, use_container_width=True, hide_index=True)

chart_scenarios = scenario_df.melt(
    id_vars="Cenário",
    value_vars=[
        "Custo por paciente (R$)",
        "Preço novos (R$)",
        "Preço amigos/família (R$)",
    ],
    var_name="Métrica",
    value_name="Valor (R$)",
)
fig_scenarios = px.bar(
    chart_scenarios,
    x="Cenário",
    y="Valor (R$)",
    color="Métrica",
    barmode="group",
)
fig_scenarios.update_layout(margin=dict(l=10, r=10, t=30, b=10))
st.plotly_chart(fig_scenarios, use_container_width=True)

p1, p2, p3, p4 = st.columns(4)
p1.metric("Contribuição — novos", brl(contrib_novos))
p2.metric("Margem sobre venda — novos", pct(margem_bruta_novos))
p3.metric("Contribuição — amigos", brl(contrib_amigos))
p4.metric("Margem sobre venda — amigos", pct(margem_bruta_amigos))

st.info(
    "O slider principal é tratado como **markup sobre custo**. "
    "A margem sobre a venda é mostrada separadamente, após custos variáveis e taxas percentuais."
)


# -----------------------------
# Estoque e investimento inicial
# -----------------------------
st.subheader("4) Estoque, investimento inicial e divisão com Julia")

# Estoque em pacientes (teórico)
capacity_rows = []
for _, row in edited.iterrows():
    qpp = float(row["Qtd/paciente"])
    if qpp > 0:
        qty_available = float(row["Qtd total"])
        # Se o item é efetivamente dividido, a Dra. Carolina também fica com sua fração do estoque.
        if bool(row["Dividido com Julia"]):
            qty_available *= share_carolina_pct / 100.0
        capacity = math.floor(qty_available / qpp)
    else:
        capacity = np.inf
    capacity_rows.append(
        {
            "Produto": row["Produto"],
            "Pacientes suportados pelo estoque": capacity,
        }
    )

tox_capacity = (
    math.floor((frascos_toxina * ui_frasco) / dose_ui) if dose_ui > 0 else 0
)
capacity_rows.append(
    {
        "Produto": f"Toxina botulínica — {tipo_toxina}",
        "Pacientes suportados pelo estoque": tox_capacity,
    }
)
capacity_df = pd.DataFrame(capacity_rows)

finite_cap = capacity_df.replace(np.inf, np.nan)["Pacientes suportados pelo estoque"].dropna()
stock_capacity = int(finite_cap.min()) if not finite_cap.empty else 0
limiting_items = capacity_df[
    capacity_df["Pacientes suportados pelo estoque"] == stock_capacity
]["Produto"].tolist()

# Investimento bruto e desembolso Carolina
invest_common_full = float(edited["Preço compra (R$)"].sum())
invest_toxin_full = preco_toxina * frascos_toxina
invest_total_full = invest_common_full + invest_toxin_full

share = share_carolina_pct / 100.0
carolina_common = float(
    np.where(
        edited["Dividido com Julia"],
        edited["Preço compra (R$)"] * share,
        edited["Preço compra (R$)"],
    ).sum()
)
carolina_toxin = invest_toxin_full
invest_carolina = carolina_common + carolina_toxin

i1, i2, i3, i4 = st.columns(4)
i1.metric("Investimento total em estoque", brl(invest_total_full))
i2.metric("Desembolso estimado da Dra.", brl(invest_carolina))
i3.metric("Capacidade do estoque atual", f"{stock_capacity} pacientes")
i4.metric(
    "Gargalo de estoque",
    ", ".join(limiting_items[:2]) + ("..." if len(limiting_items) > 2 else ""),
)

with st.expander("Ver capacidade por item"):
    cap_show = capacity_df.copy()
    cap_show["Pacientes suportados pelo estoque"] = cap_show[
        "Pacientes suportados pelo estoque"
    ].apply(lambda x: "∞" if x == np.inf else int(x))
    st.dataframe(cap_show, use_container_width=True, hide_index=True)


# -----------------------------
# Breakeven
# -----------------------------
st.subheader("5) Breakeven e projeção mensal")

# Três leituras diferentes:
# 1) BE operacional: cobre custos fixos recorrentes com contribuição por paciente
# 2) BE sustentável + payback: cobre fixos + parcela mensal do investimento, preservando reposição
# 3) Recuperação bruta de caixa: receita bruta necessária para recompor desembolso inicial
be_operacional = safe_ceil_div(custo_fixo_mensal, contrib_novos)
parcela_investimento = invest_carolina / meses_payback
be_payback = safe_ceil_div(custo_fixo_mensal + parcela_investimento, contrib_novos)
be_caixa_bruto = safe_ceil_div(invest_carolina, preco_novos)

b1, b2, b3 = st.columns(3)
b1.metric(
    "BE operacional/mês",
    f"{be_operacional} pacientes" if be_operacional is not None else "—",
    help="Pacientes necessários para cobrir os custos fixos mensais.",
)
b2.metric(
    f"BE + payback em {meses_payback} mês(es)",
    f"{be_payback} pacientes/mês" if be_payback is not None else "—",
    help="Cobre fixos e recupera o desembolso inicial no prazo escolhido, mantendo reserva para reposição.",
)
b3.metric(
    "Pacientes p/ recompor caixa inicial",
    f"{be_caixa_bruto} pacientes" if be_caixa_bruto is not None else "—",
    help="Leitura simples de caixa: investimento inicial dividido pela receita bruta por paciente.",
)

receita_mes = pacientes_mes * preco_novos
taxas_mes = receita_mes * fee
custo_variavel_mes = pacientes_mes * custo_realista
contribuicao_mes = receita_mes - taxas_mes - custo_variavel_mes
resultado_operacional_mes = contribuicao_mes - custo_fixo_mensal
resultado_apos_payback_alvo = resultado_operacional_mes - parcela_investimento

m1, m2, m3, m4 = st.columns(4)
m1.metric("Receita mensal projetada", brl(receita_mes))
m2.metric("Custo variável mensal", brl(custo_variavel_mes))
m3.metric("Resultado operacional", brl(resultado_operacional_mes))
m4.metric(
    "Resultado após parcela de payback",
    brl(resultado_apos_payback_alvo),
)

max_patients_chart = max(30, int(pacientes_mes * 2), (be_payback or 0) + 10)
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
        "Resultado após custos e payback (R$)": profit_curve,
    }
)
fig_be = px.line(
    be_curve_df,
    x="Pacientes/mês",
    y="Resultado após custos e payback (R$)",
    markers=True,
)
fig_be.add_hline(y=0, line_dash="dash")
fig_be.update_layout(margin=dict(l=10, r=10, t=30, b=10))
st.plotly_chart(fig_be, use_container_width=True)


# -----------------------------
# Comparação 100 UI x 200 UI
# -----------------------------
st.subheader("6) Comparativo econômico dos frascos de toxina")

comparison = pd.DataFrame(
    [
        {
            "Frasco": "100 UI",
            "Preço do frasco (R$)": preco_toxina_100,
            "Dose por paciente (UI)": dose_ui,
            "Custo teórico da toxina/paciente (R$)": preco_toxina_100 * dose_ui / 100.0,
            "Pacientes teóricos por frasco": math.floor(100.0 / dose_ui),
        },
        {
            "Frasco": "200 UI",
            "Preço do frasco (R$)": preco_toxina_200,
            "Dose por paciente (UI)": dose_ui,
            "Custo teórico da toxina/paciente (R$)": preco_toxina_200 * dose_ui / 200.0,
            "Pacientes teóricos por frasco": math.floor(200.0 / dose_ui),
        },
    ]
)
comparison["Ativo no cálculo"] = comparison["Frasco"].eq(tipo_toxina)

comparison_display = comparison.copy()
comparison_display["Preço do frasco (R$)"] = comparison_display["Preço do frasco (R$)"].map(brl)
comparison_display["Custo teórico da toxina/paciente (R$)"] = comparison_display[
    "Custo teórico da toxina/paciente (R$)"
].map(brl)

st.dataframe(comparison_display, use_container_width=True, hide_index=True)

best_row = comparison.loc[
    comparison["Custo teórico da toxina/paciente (R$)"].idxmin()
]
st.success(
    f"Com os preços atuais, o frasco economicamente mais barato por paciente é "
    f"**{best_row['Frasco']}**, com custo teórico de "
    f"**{brl(best_row['Custo teórico da toxina/paciente (R$)'])}** de toxina por aplicação."
)


# -----------------------------
# Exportação
# -----------------------------
st.subheader("7) Exportar resultados")

export_costs = cost_detail.copy()
export_scenarios = scenario_df.copy()
export_breakeven = pd.DataFrame(
    [
        {"Indicador": "Custo base calculado", "Valor": custo_base_calculado},
        {"Indicador": "Custo base + adicionais", "Valor": custo_base_total},
        {"Indicador": "Custo realista", "Valor": custo_realista},
        {"Indicador": "Preço novos", "Valor": preco_novos},
        {"Indicador": "Preço amigos/família", "Valor": preco_amigos},
        {"Indicador": "Investimento total em estoque", "Valor": invest_total_full},
        {"Indicador": "Desembolso estimado da Dra.", "Valor": invest_carolina},
        {"Indicador": "BE operacional (pacientes/mês)", "Valor": be_operacional},
        {
            "Indicador": f"BE + payback em {meses_payback} mês(es)",
            "Valor": be_payback,
        },
        {"Indicador": "Resultado operacional mensal", "Valor": resultado_operacional_mes},
    ]
)

csv = export_breakeven.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
st.download_button(
    "Baixar resumo em CSV",
    data=csv,
    file_name="resumo_financeiro_botox.csv",
    mime="text/csv",
)

st.caption(
    "Modelo financeiro gerencial. Valide custos tributários, regras de cobrança, "
    "políticas de retoque e demais despesas reais antes de definir o preço final."
)
