import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(__file__))
from src.setup_db import criar_base_de_dados
from src.metrics_sql import (
    receita_total,
    lucro_total,
    total_transacoes,
    produto_mais_vendido,
    vendas_por_produto,
    vendas_por_periodo,
    margem_por_produto,
    vendas_filtradas,
)

# ── Configuração da página ──────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)

# ── Caminhos ────────────────────────────────────────────────────────
CSV_PATH = "data/vendas.csv"
DB_PATH  = "data/vendas.db"

# Cria a base de dados se não existir
if not os.path.exists(DB_PATH):
    criar_base_de_dados(CSV_PATH, DB_PATH)

# ── Carregar datas disponíveis para o filtro ────────────────────────
import sqlite3, pandas as pd
conn = sqlite3.connect(DB_PATH)
datas_df = pd.read_sql_query("SELECT MIN(data) AS min, MAX(data) AS max FROM vendas", conn)
conn.close()

data_min = pd.to_datetime(datas_df["min"].iloc[0]).date()
data_max = pd.to_datetime(datas_df["max"].iloc[0]).date()

# ── Título ──────────────────────────────────────────────────────────
st.title("📊 Dashboard de Vendas")
st.markdown("Análise de receita, lucro e performance por produto e período.")
st.divider()

# ── Filtro por período ──────────────────────────────────────────────
st.sidebar.header("🔍 Filtros")
datas = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

if isinstance(datas, (list, tuple)) and len(datas) == 2:
    inicio = str(datas[0])
    fim    = str(datas[1])
elif hasattr(datas, '__len__') and len(datas) == 1:
    inicio = str(datas[0])
    fim    = str(datas[0])
else:
    inicio = str(data_min)
    fim    = str(data_max)

# ── KPIs principais (com filtro de data via SQL) ────────────────────
df_filtrado = vendas_filtradas(DB_PATH, inicio, fim)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Receita Total",  f"€{df_filtrado['receita'].sum():,.2f}")
col2.metric("📈 Lucro Total",    f"€{df_filtrado['lucro'].sum():,.2f}")
col3.metric("🧾 Transações",     len(df_filtrado))
col4.metric("🏆 Mais Lucrativo", df_filtrado.groupby("produto")["receita"].sum().idxmax())

st.divider()

# ── Gráficos ────────────────────────────────────────────────────────
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Receita por Produto")
    dados_produto = vendas_por_produto(DB_PATH)
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
    dados_periodo = vendas_por_periodo(DB_PATH)
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
margem = margem_por_produto(DB_PATH)
st.dataframe(
    margem.style.format({
        "receita_total": "€{:.2f}",
        "lucro_total":   "€{:.2f}",
        "margem_pct":    "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)