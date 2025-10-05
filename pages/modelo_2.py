import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import  formatar_inteiro

# ===============================
# Configuração da Página
# ===============================
st.set_page_config(
    page_title="Análise de Conversão de Vendas",
    page_icon=":material/target:",
    layout="wide"
)

# ===============================
# Carregamento do Modelo e Encoders
# ===============================
@st.cache_resource
def load_assets(model_path, encoder_paths):
    """Carrega o modelo de classificação e os encoders a partir de arquivos .pkl"""
    assets = {}
    try:
        assets['model'] = joblib.load(model_path)
        for name, path in encoder_paths.items():
            assets[name] = joblib.load(path)
        return assets
    except FileNotFoundError as e:
        st.error(f":material/error: Arquivo não encontrado: {e.filename}. Por favor, adicione o arquivo na pasta do projeto e atualize a página.")
        st.stop()

ENCODER_PATHS = {
    "le_main_category": "./encoders/le_main_category.pkl",
    "le_brand": "./encoders/le_brand.pkl",
    "le_weekday": "./encoders/le_weekday.pkl"
}
assets = load_assets("./models/modelo_randomforest.pkl", ENCODER_PATHS)
classification_model = assets['model']

# ===============================
# Sidebar e Upload de Arquivo
# ===============================
with st.sidebar:
    with st.expander(":material/upload: Upload de CSV", expanded=False):
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

        st.markdown("""
        **Critérios para o CSV:**
        - Deve conter as **colunas já codificadas (numéricas)**.
        - Ex: `price`, `brand_encoded`, `main_category_encoded`, `sub_category_encoded`, `hour`, `weekday_encoded`, `add_to_cart_count`, `views_count`.
        """)

# ===============================
# Carregamento dos Dados
# ===============================
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Carregando dados de exemplo de um arquivo CSV
    try:
        df = pd.read_csv("./datasets/randomforest_test.csv")
        st.info(":material/info: Nenhum arquivo enviado. Usando dados de exemplo do arquivo df_tratado_streamlit.csv.")
    except FileNotFoundError:
        st.error(":material/error: Arquivo de exemplo não encontrado. Por favor, faça upload de um arquivo CSV.")
        st.stop()

# ===============================
# Título e Amostra dos Dados
# ===============================
st.markdown('<h1 style="color:#1a73e8;">Modelo 2 - Previsão de Probabilidade de Compra</h1>', unsafe_allow_html=True)
with st.expander("Visualizar Amostra dos Dados "):
    st.dataframe(df.head(5))

# ===============================
# 2. Predição e Decodificação para Gráficos
# ===============================
with st.spinner('Aplicando o modelo e preparando visualizações...'):
    df_processed = df.copy()

    # 1. Seleção de Features para o Modelo
    features = [
        "price", "brand_encoded", "main_category_encoded", "sub_category_encoded",
        "hour", "weekday_encoded", "add_to_cart_count", "views_count"
    ]
    # Validação se as colunas existem
    if not all(col in df_processed.columns for col in features):
        st.error(f":material/error: O CSV precisa conter todas as colunas necessárias: {', '.join(features)}")
        st.stop()

    X = df_processed[features]

    # 2. Predição com o Modelo
    y_probs = classification_model.predict_proba(X)[:, 1]
    df_processed['prob_compra'] = y_probs
    
    threshold = 0.3
    df_processed['predicao'] = (df_processed['prob_compra'] >= threshold).astype(int)
    df_processed['classificacao'] = df_processed['predicao'].apply(lambda x: "Potencial Conversão" if x == 1 else "Baixo Potencial")

    # 3. DECODIFICAÇÃO (inverse_transform): Criando colunas de texto para os gráficos
    try:
        df_processed['brand'] = assets['le_brand'].inverse_transform(df_processed['brand_encoded'])
        df_processed['main_category'] = assets['le_main_category'].inverse_transform(df_processed['main_category_encoded'])
        df_processed['weekday'] = assets['le_weekday'].inverse_transform(df_processed['weekday_encoded'])
    except Exception as e:
        st.error(f":material/error: Erro ao decodificar os dados para os gráficos: **{e}**")
        st.warning("Isso pode acontecer se os códigos numéricos no seu CSV não corresponderem aos códigos usados no treinamento do modelo.")
        st.stop()

st.success(":material/check_circle: Predição concluída! Gráficos gerados com sucesso.")


st.divider()
st.subheader(":material/analytics: Análise de Conversão")

df_conversao = df_processed[df_processed['classificacao'] == "Potencial Conversão"]


# --- INÍCIO DO CÓDIGO DOS GRÁFICOS
st.markdown("**História de Negócio:** Como gerente de vendas, quero analisar os registros de sessões para classificá-las como possibilidade de conversão, permitindo focar esforços de marketing e vendas nos clientes mais promissores.")

total_sessoes = len(df_processed)
sessoes_potenciais = len(df_conversao)
perc_potencial = (sessoes_potenciais / total_sessoes) * 100 if total_sessoes > 0 else 0

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Total de Sessões Analisadas", formatar_inteiro(total_sessoes))
    st.metric("Sessões com Potencial de Conversão", formatar_inteiro(sessoes_potenciais))
    st.metric("Taxa de Potencial de Conversão", f"{perc_potencial:.2f}%")

with col2:
    fig_pie = px.pie(
        df_processed,
        names='classificacao',
        title='Distribuição das Sessões por Potencial de Conversão',
        color='classificacao',
        color_discrete_map={'Potencial Conversão': 'lightgreen', 'Baixo Potencial': 'lightcoral'}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("#### :material/shopping_cart: Marcas e Categorias com Maior Potencial de Venda")
st.markdown("**História de Negócio:** Como gerente de vendas, quero visualizar as marcas e categorias com a maior possibilidade de conversão para direcionar campanhas, otimizar estoques e negociar com fornecedores estratégicos.")

col3, col4 = st.columns(2)

with col3:
    top_marcas = df_conversao['brand'].value_counts().nlargest(10).reset_index()
    fig_marcas = px.bar(
        top_marcas,
        x='count',
        y='brand',
        orientation='h',
        title='Top 10 Marcas em Sessões de Potencial Conversão',
        labels={'count': 'Nº de Sessões', 'brand': 'Marca'},
        text='count'
    )
    fig_marcas.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_marcas, use_container_width=True)

with col4:
    top_categorias = df_conversao['main_category'].value_counts().nlargest(10).reset_index()
    fig_categorias = px.bar(
        top_categorias,
        x='count',
        y='main_category',
        orientation='h',
        title='Top 10 Categorias em Sessões de Potencial Conversão',
        labels={'count': 'Nº de Sessões', 'main_category': 'Categoria'},
        text='count'
    )
    fig_categorias.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_categorias, use_container_width=True)

st.markdown("#### :material/calendar_today: Dias da Semana Mais Propensos à Conversão")
st.markdown("**História de Negócio:** Como gerente de vendas, quero saber quais dias da semana são mais propensos a resultar em uma compra para otimizar o agendamento de campanhas de marketing, promoções e a escala da equipe de atendimento.")

dias_conversao = df_conversao['weekday'].value_counts().reset_index()
ordem_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dias_conversao['weekday'] = pd.Categorical(dias_conversao['weekday'], categories=ordem_dias, ordered=True)
dias_conversao = dias_conversao.sort_values('weekday')

fig_dias = px.bar(
    dias_conversao,
    x='weekday',
    y='count',
    title='Sessões com Potencial de Conversão por Dia da Semana',
    labels={'count': 'Nº de Sessões', 'weekday': 'Dia da Semana'},
    text='count'
)
st.plotly_chart(fig_dias, use_container_width=True)

st.divider()
st.subheader(":material/download: Download dos Resultados")
csv = df_processed.to_csv(index=False).encode('utf-8')
st.download_button(
    label=":material/save: Baixar Dados com Predições (CSV)",
    data=csv,
    file_name="purchase_predictions_resultados.csv",
    mime="text/csv"
)
