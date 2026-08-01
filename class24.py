"""
Mini Dashboard em Python com Streamlit
----------------------------------------
Como executar:
    1. pip install streamlit pandas plotly
    2. streamlit run mini_dashboard.py

O dashboard usa dados de vendas fictícios, mas você pode substituir
pela leitura de um CSV/Excel/banco de dados real (veja o comentário
na seção "CARREGAR DADOS").
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ----------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Mini Dashboard",
    page_icon="📊",
    layout="wide",
)

# ----------------------------------------------------------------
# CARREGAR DADOS
# ----------------------------------------------------------------
@st.cache_data
def carregar_dados():
    # Substitua este bloco por: pd.read_csv("seu_arquivo.csv")
    np.random.seed(42)
    dias = pd.date_range(end=datetime.today(), periods=180)
    regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    produtos = ["Produto A", "Produto B", "Produto C", "Produto D"]

    dados = []
    for dia in dias:
        for _ in range(np.random.randint(5, 15)):
            dados.append({
                "data": dia,
                "regiao": np.random.choice(regioes),
                "produto": np.random.choice(produtos),
                "vendas": np.random.randint(50, 500),
                "quantidade": np.random.randint(1, 20),
            })
    return pd.DataFrame(dados)

df = carregar_dados()

# ----------------------------------------------------------------
# BARRA LATERAL — FILTROS
# ----------------------------------------------------------------
st.sidebar.title("🔎 Filtros")

data_min, data_max = df["data"].min(), df["data"].max()
intervalo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
)

regioes_sel = st.sidebar.multiselect(
    "Região", options=sorted(df["regiao"].unique()), default=sorted(df["regiao"].unique())
)

produtos_sel = st.sidebar.multiselect(
    "Produto", options=sorted(df["produto"].unique()), default=sorted(df["produto"].unique())
)

if len(intervalo) == 2:
    inicio, fim = intervalo
else:
    inicio, fim = data_min, data_max

df_filtrado = df[
    (df["data"] >= pd.to_datetime(inicio))
    & (df["data"] <= pd.to_datetime(fim))
    & (df["regiao"].isin(regioes_sel))
    & (df["produto"].isin(produtos_sel))
]

# ----------------------------------------------------------------
# TÍTULO
# ----------------------------------------------------------------
st.title("📊 Mini Dashboard de Vendas")
st.caption(f"Dados de {inicio} até {fim}")

# ----------------------------------------------------------------
# KPIs (CARTÕES DE MÉTRICAS)
# ----------------------------------------------------------------
total_vendas = df_filtrado["vendas"].sum()
total_qtd = df_filtrado["quantidade"].sum()
ticket_medio = total_vendas / total_qtd if total_qtd else 0
n_pedidos = len(df_filtrado)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Receita Total", f"R$ {total_vendas:,.2f}")
col2.metric("📦 Itens Vendidos", f"{total_qtd:,}")
col3.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}")
col4.metric("🧾 Nº de Pedidos", f"{n_pedidos:,}")

st.divider()

# ----------------------------------------------------------------
# GRÁFICOS
# ----------------------------------------------------------------
col_a, col_b = st.columns(2)

with col_a:
    vendas_por_dia = df_filtrado.groupby("data")["vendas"].sum().reset_index()
    fig_linha = px.line(
        vendas_por_dia, x="data", y="vendas",
        title="Evolução da Receita ao Longo do Tempo",
        markers=True,
    )
    st.plotly_chart(fig_linha, use_container_width=True)

with col_b:
    vendas_por_regiao = df_filtrado.groupby("regiao")["vendas"].sum().reset_index()
    fig_barra = px.bar(
        vendas_por_regiao, x="regiao", y="vendas",
        title="Receita por Região", color="regiao",
    )
    st.plotly_chart(fig_barra, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    vendas_por_produto = df_filtrado.groupby("produto")["vendas"].sum().reset_index()
    fig_pizza = px.pie(
        vendas_por_produto, names="produto", values="vendas",
        title="Participação por Produto", hole=0.4,
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

with col_d:
    fig_dispersao = px.scatter(
        df_filtrado, x="quantidade", y="vendas", color="produto",
        title="Quantidade vs. Receita", opacity=0.6,
    )
    st.plotly_chart(fig_dispersao, use_container_width=True)

st.divider()

# ----------------------------------------------------------------
# TABELA DE DADOS
# ----------------------------------------------------------------
st.subheader("📋 Dados Detalhados")
st.dataframe(
    df_filtrado.sort_values("data", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "⬇️ Baixar dados filtrados (CSV)",
    data=df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="dados_filtrados.csv",
    mime="text/csv",
)