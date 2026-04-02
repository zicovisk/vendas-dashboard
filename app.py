import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(__file__))
from src.load_data import load_vendas
from src.metrics import (
    receita_total,
    lucro_total,
    total_transacoes,
    produto_mais_vendido,
    vendas_por_produto,
    vendas_por_periodo,
    margem_por_produto,
)

# ── Configuração da página ──────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)

# ── Carregar dados ──────────────────────────────────────────────────
@st.cache_data
def carregar():
    return load_vendas("data/vendas.csv")

df = carregar()

# ── Título ──────────────────────────────────────────────────────────
st.title("📊 Dashboard de Vendas")
st.markdown("Análise de receita, lucro e performance por produto e período.")
st.divider()

# ── Filtro por período ──────────────────────────────────────────────
st.sidebar.header("🔍 Filtros")
datas = st.sidebar.date_input(
    "Período",
    value=(df["data"].min(), df["data"].max()),
    min_value=df["data"].min(),
    max_value=df["data"].max()
)

if len(datas) == 2:
    df_filtrado = df[
        (df["data"] >= str(datas[0])) &
        (df["data"] <= str(datas[1]))
    ]
else:
    df_filtrado = df

# ── KPIs principais ─────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Receita Total", f"€{receita_total(df_filtrado):,.2f}")
col2.metric("📈 Lucro Total", f"€{lucro_total(df_filtrado):,.2f}")
col3.metric("🧾 Transações", total_transacoes(df_filtrado))
col4.metric("🏆 Mais Vendido", produto_mais_vendido(df_filtrado))

st.divider()

# ── Gráficos ────────────────────────────────────────────────────────
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Receita por Produto")
    dados_produto = vendas_por_produto(df_filtrado)
    fig1 = px.bar(
        dados_produto,
        x="produto",
        y="receita_total",
        color="produto",
        labels={"receita_total": "Receita (€)", "produto": "Produto"},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_dir:
    st.subheader("Evolução Mensal")
    dados_periodo = vendas_por_periodo(df_filtrado)
    fig2 = px.line(
        dados_periodo,
        x="mes",
        y=["receita", "lucro"],
        markers=True,
        labels={"value": "€", "mes": "Mês", "variable": "Métrica"},
        color_discrete_map={"receita": "#636EFA", "lucro": "#00CC96"}
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Tabela de margem ────────────────────────────────────────────────
st.subheader("📋 Margem por Produto")
margem = margem_por_produto(df_filtrado)
st.dataframe(
    margem.style.format({
        "receita_total": "€{:.2f}",
        "lucro_total": "€{:.2f}",
        "margem_pct": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)
