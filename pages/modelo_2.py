import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# ===============================
# 1. Carregar Dataset
# ===============================
df = pd.read_csv("pages\customer_clusters.csv")

st.set_page_config(
    page_title="Análise de Clientes",
    page_icon=":bar_chart:",
    layout="wide"
)

st.markdown('<h1 style="color:#1a73e8;">Análise de Clientes - Clusterização</h1>', unsafe_allow_html=True)

with st.expander("📊 Dados do Dataset"):
    st.dataframe(df.head(5))

# ===============================
# 2. Pré-processamento + Clusterização
# ===============================
X = df[["total_spent", "frequency", "recency_days"]].copy()

# Normalização
X_scaled = (X - X.mean()) / X.std()
X_scaled["recency_days"] = X_scaled["recency_days"].fillna(1000)

# KMeans
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

# Resumo por cluster
cluster_summary = df.groupby("cluster").agg(
    avg_spent=("total_spent", "mean"),
    total_spent=("total_spent", "sum"),
    customers=("user_id", "count"),
    avg_frequency=("frequency", "mean"),
    avg_recency=("recency_days", "mean")
).reset_index()

# ===============================
# 3. Sidebar - Filtros
# ===============================
st.sidebar.header(":material/search: Filtros de Análise")

clusters_disponiveis = ["Todos"] + sorted(df["cluster"].unique().tolist())
cluster_selecionado = st.sidebar.selectbox("Selecione o Cluster:", clusters_disponiveis)

df_filtrado = df.copy()
if cluster_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["cluster"] == cluster_selecionado]

if cluster_selecionado != "Todos":
    st.info(f"🔎 Filtro aplicado: Cluster {cluster_selecionado} | Total clientes: {len(df_filtrado):,}")

# ===============================
# 4. Métricas Principais
# ===============================
st.subheader(":material/insights: Métricas Gerais")

total_clientes = len(df_filtrado)
total_spent = df_filtrado["total_spent"].sum()
gasto_medio = df_filtrado["total_spent"].mean()
freq_media = df_filtrado["frequency"].mean()
recencia_media = df_filtrado["recency_days"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Clientes", f"{total_clientes:,}")
col2.metric("Gasto Total", f"R$ {total_spent:,.2f}")
col3.metric("Gasto Médio", f"R$ {gasto_medio:,.2f}")
col4.metric("Frequência Média", f"{freq_media:.1f}")
col5.metric("Recência Média (dias)", f"{recencia_media:.1f}")

st.divider()

# ===============================
# 5. Gráficos
# ===============================

# Gráfico de clusters por gasto total
st.markdown("**História de Negócio:** Como gerente financeiro, eu quero identificar quais clusters geram mais receita para priorizar investimentos.")
st.subheader(":material/bar_chart: Gasto Total por Cluster")
fig1 = px.bar(
    cluster_summary.sort_values("total_spent", ascending=False),
    x="cluster", y="total_spent",
    text_auto=".2s",
    labels={"cluster": "Cluster", "total_spent": "Gasto Total"},
    color="cluster"
)
st.plotly_chart(fig1, use_container_width=True)

# Distribuição de clientes por cluster
st.markdown("**História de Negócio:** Como gerente de marketing, eu quero saber a proporção de clientes em cada cluster para planejar campanhas segmentadas.")
st.subheader(":material/pie_chart: Distribuição de Clientes por Cluster")
fig2 = px.pie(
    cluster_summary,
    values="customers", names="cluster",
    title="Participação de Clientes por Cluster"
)
st.plotly_chart(fig2, use_container_width=True)

# Relação gasto x frequência (scatter)
st.markdown("**História de Negócio:** Como analista de CRM, eu quero visualizar a relação entre gasto e frequência para identificar clientes de alto valor.")
st.subheader(":material/scatter_plot: Relação Gasto x Frequência")
fig3 = px.scatter(
    df_filtrado, x="frequency", y="total_spent",
    color="cluster", hover_data=["user_id"],
    title="Dispersão de Clientes"
)
st.plotly_chart(fig3, use_container_width=True)

# Boxplot - recência por cluster
st.markdown("**História de Negócio:** Como gerente de retenção, eu quero entender a recência dos clientes em cada cluster para definir estratégias de reativação.")
st.subheader(":material/bar_chart: Distribuição de Recência por Cluster")
fig4 = px.box(
    df_filtrado, x="cluster", y="recency_days",
    color="cluster", points="all",
    title="Distribuição da Recência"
)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ===============================
# 6. Download
# ===============================
st.subheader(":material/download: Download dos Resultados")
csv = df.to_csv(index=False)
st.download_button(
    label=":material/file_download: Baixar Dados com Clusters (CSV)",
    data=csv,
    file_name="customer_clusters_resultados.csv",
    mime="text/csv"
)
