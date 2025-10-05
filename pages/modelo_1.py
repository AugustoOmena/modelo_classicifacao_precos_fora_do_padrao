from sklearn.preprocessing import StandardScaler
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import formatar_moeda, formatar_numero

st.set_page_config(
    page_title="Análise de Clientes",
    page_icon=":bar_chart:",
    layout="wide"
)

# ===============================
# Upload CSV em Acordeon
# ===============================
with st.sidebar.expander(":material/upload: Upload de CSV", expanded=False):
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    st.markdown("""
    **Critérios para o CSV funcionar:**
    - Deve conter as colunas:
      - `user_id` (identificador único do cliente)
      - `total_spent` (numérica)
      - `frequency` (numérica)
      - `recency_days` (numérica)
    - Os valores não podem estar vazios nessas colunas.
    - Arquivo no formato **CSV** com separador padrão `,`.
    """)

# ===============================
# Carregar dataset
# ===============================
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    colunas_necessarias = ["user_id", "total_spent", "frequency", "recency_days"]
    colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]
    if colunas_faltando:
        st.error(f":material/error: O arquivo enviado não possui as colunas necessárias: {', '.join(colunas_faltando)}")
        st.stop()
    else:
        st.success(":material/check_circle: Dataset válido! Todas as colunas obrigatórias estão presentes.")
else:
    df = pd.read_csv("./datasets/cluster_test.csv")
    st.info(":material/info: Nenhum arquivo enviado. Usando dataset padrão **cluster_test.csv**.")


st.markdown('<h1 style="color:#1a73e8;">Modelo 1 - Análise de Clientes - Clusterização</h1>', unsafe_allow_html=True)

with st.expander("Visualizar Amostra dos Dados"):
    st.dataframe(df.head(5))

# ===============================
# 2. Pré-processamento + Clusterização
# ===============================
@st.cache_resource
def load_model(path):
    """Carrega o modelo K-Means a partir de um arquivo .pkl"""
    try:
        model = joblib.load(path)
        return model
    except FileNotFoundError:
        return None

# Carrega o modelo treinado pelo seu amigo
kmeans_model = load_model("./models/modelo_kmeans.pkl")

# Validação para ver se o modelo foi carregado corretamente
if kmeans_model is None:
    st.error(":material/error: Arquivo 'modelo_kmeans.pkl' não encontrado. Por favor, adicione o arquivo do modelo na pasta do projeto e atualize a página.")
    st.stop()
else:
    st.success(":material/check_circle: Modelo de clusterização `modelo_kmeans.pkl` carregado com sucesso!")

# Escalonamento de Features
scaler = StandardScaler()

X = df[["total_spent", "frequency", "recency_days"]]

X_scaled = scaler.fit_transform(X)

df["cluster"] = kmeans_model.predict(X_scaled)

# Resumo por cluster
cluster_summary = df.groupby("cluster").agg(
    avg_spent=("total_spent", "mean"),
    total_spent=("total_spent", "sum"),
    customers=("user_id", "count")
).reset_index()

# ===============================
# 3. Sidebar
# ===============================
st.sidebar.header(":material/search: Filtros de Análise")

clusters_disponiveis = ["Todos"] + sorted(df["cluster"].unique().tolist())
cluster_selecionado = st.sidebar.selectbox("Selecione o Cluster:", clusters_disponiveis)

df_filtrado = df.copy()
if cluster_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["cluster"] == cluster_selecionado]

if cluster_selecionado != "Todos":
    st.info(f":material/search: Filtro aplicado: Cluster {cluster_selecionado} | Total clientes: {formatar_numero(len(df_filtrado))}")
else:
    st.info(f":material/search: Filtro aplicado: Todos os Clusters | Total clientes: {formatar_numero(len(df_filtrado))}")

# ===============================
# 4. Métricas Principais
# ===============================
st.subheader(":material/insights: Métricas Gerais")
st.markdown("Visão geral dos principais indicadores de comportamento do cliente, com base nos filtros selecionados. Essas métricas nos ajudam a ter um panorama rápido e a aprofundar a análise.")

total_clientes = len(df_filtrado)
total_spent = df_filtrado["total_spent"].sum()
gasto_medio = df_filtrado["total_spent"].mean()
freq_media = df_filtrado["frequency"].mean()
recencia_media = df_filtrado["recency_days"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Clientes", formatar_numero(total_clientes))
col2.metric("Gasto Total", formatar_moeda(total_spent))
col3.metric("Gasto Médio", formatar_moeda(gasto_medio))

st.divider()

# ===============================
# 5. Gráficos 
# ===============================
st.subheader(":material/bar_chart: Gasto Total por Cluster")
st.markdown("**História de Negócio:** Como gerente de vendas, busco entender a contribuição de cada cluster para a receita total. Este gráfico nos permite identificar os grupos de clientes mais lucrativos, direcionando os investimentos de forma mais estratégica e otimizando o retorno sobre o marketing.")
fig1 = px.bar(
    cluster_summary.sort_values("total_spent", ascending=False),
    x="cluster", y="total_spent",
    text_auto=".2s",
    labels={"cluster": "Cluster", "total_spent": "Gasto Total"},
    color="cluster"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader(":material/pie_chart: Distribuição de Clientes por Cluster")
st.markdown("**História de Negócio:** Como gerente de marketing, preciso visualizar a distribuição dos nossos clientes entre os diferentes clusters. Compreender o tamanho de cada segmento é fundamental para o planejamento de campanhas de marketing personalizadas e a alocação de recursos, garantindo que nossas mensagens alcancem o público certo.")
fig2 = px.pie(
    cluster_summary,
    values="customers", names="cluster",
    title="Participação de Clientes por Cluster"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader(":material/scatter_plot: Relação Gasto x Frequência")
st.markdown("**História de Negócio:** Como analista de CRM, meu objetivo é identificar padrões de comportamento que definem nossos clientes de maior valor. Este gráfico de dispersão cruza o valor gasto com a frequência de compra, nos ajudando a visualizar e a entender quem são os clientes que sustentam o negócio e como podemos criar programas de fidelidade mais eficazes.")
fig3 = px.scatter(
    df_filtrado, x="frequency", y="total_spent",
    color="cluster", hover_data=["user_id"],
    title="Dispersão de Clientes"
)
st.plotly_chart(fig3, use_container_width=True)

# Boxplot - recência por cluster
st.subheader(":material/bar_chart: Distribuição de Recência por Cluster")
st.markdown("**História de Negócio:** Como gerente de vendas, preciso monitorar a 'saúde' do relacionamento com nossos clientes. Este gráfico mostra há quanto tempo os clientes de cada cluster fizeram sua última compra. Identificar clusters com alta recência (muito tempo desde a última compra) é crucial para desenvolvermos campanhas de reativação e prevenirmos a perda de clientes.")
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