import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go

# Carregar o arquivo X_test.csv
df = pd.read_csv('X_test_brand_mcategory.csv')

st.markdown('<h1 style="color:#1a73e8;">Modelo 1 - Classificação - Preços fora do Padrão</h1>', unsafe_allow_html=True)

with st.expander("Dados do Dataset"):
    st.dataframe(df.head(4))

# Sidebar para filtros
st.sidebar.header("🔍 Filtros de Análise")

# Obter valores únicos para filtros
categorias_disponiveis = ['Todas'] + sorted(df['main_category'].unique().tolist())
marcas_disponiveis = ['Todas'] + sorted(df['brand'].unique().tolist())

# Filtros
categoria_selecionada = st.sidebar.selectbox(
    "Selecione a Categoria:",
    categorias_disponiveis
)

marca_selecionada = st.sidebar.selectbox(
    "Selecione a Marca:",
    marcas_disponiveis
)

# Aplicar filtros
df_filtrado = df.copy()

if categoria_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['main_category'] == categoria_selecionada]

if marca_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['brand'] == marca_selecionada]

# Mostrar informações dos filtros aplicados
if categoria_selecionada != 'Todas' or marca_selecionada != 'Todas':
    st.info(f"📊 Filtros aplicados: Categoria: {categoria_selecionada} | Marca: {marca_selecionada}")
    st.info(f"📈 Total de produtos após filtros: {len(df_filtrado):,}")

# Layout em colunas para o botão e estatísticas
col1, col2, col3 = st.columns([2, 1, 1])

with col2:
    if st.button("🔄 Analisar Preços", type="primary", use_container_width=True):
        # Carregar o modelo
        with open('logistic_regression_model.pkl', 'rb') as file:
            model = pickle.load(file)
        
        # Selecionar apenas as colunas que o modelo foi treinado
        df_model = df_filtrado[['price', 'price_ratio_cat']]
        
        # Aplicar o modelo aos dados filtrados
        predictions = model.predict(df_model)
        
        # Adicionar predições ao DataFrame filtrado
        df_resultado = df_filtrado.copy()
        df_resultado['classificacao'] = predictions
        df_resultado['status_preco'] = df_resultado['classificacao'].map({
            0: 'Preço Normal',
            1: 'Preço fora do Padrão'
        })
        
        # Armazenar resultado no session_state
        st.session_state.df_resultado = df_resultado
        st.session_state.analise_feita = True

with col3:
    if st.button("🔄 Limpar Análise", type="secondary", use_container_width=True):
        if 'df_resultado' in st.session_state:
            del st.session_state.df_resultado
        if 'analise_feita' in st.session_state:
            del st.session_state.analise_feita
        st.rerun()

# Verificar se análise foi feita
if 'analise_feita' in st.session_state and st.session_state.analise_feita:
    df_resultado = st.session_state.df_resultado
    
    # Métricas principais
    total_produtos = len(df_resultado)
    produtos_fora_padrao = len(df_resultado[df_resultado['classificacao'] == 1])
    percentual_fora_padrao = (produtos_fora_padrao / total_produtos * 100) if total_produtos > 0 else 0
    
    # Exibir métricas
    met1, met2, met3, met4 = st.columns(4)
    with met1:
        st.metric("Total de Produtos", f"{total_produtos:,}")
    with met2:
        st.metric("Produtos fora do Padrão", f"{produtos_fora_padrao:,}")
    with met3:
        st.metric("% fora do Padrão", f"{percentual_fora_padrao:.1f}%")
    with met4:
        preco_medio_fora = df_resultado[df_resultado['classificacao'] == 1]['price'].mean()
        st.metric("Preço Médio (fora padrão)", f"R$ {preco_medio_fora:.2f}" if not pd.isna(preco_medio_fora) else "N/A")
    
    st.divider()
    
    # Análise por categoria - Gráfico de colunas
    st.subheader("📊 Produtos fora do Padrão por Categoria")
    
    analise_categoria = df_resultado.groupby(['main_category', 'status_preco']).size().unstack(fill_value=0)
    
    if 'Preço fora do Padrão' in analise_categoria.columns:
        analise_categoria_sorted = analise_categoria.sort_values('Preço fora do Padrão', ascending=False)
        
        fig_categoria = px.bar(
            analise_categoria_sorted.reset_index(), 
            x='main_category', 
            y=['Preço Normal', 'Preço fora do Padrão'],
            title="Distribuição de Preços por Categoria",
            labels={'main_category': 'Categoria', 'value': 'Quantidade de Produtos'},
            color_discrete_map={
                'Preço Normal': '#2E8B57',
                'Preço fora do Padrão': '#DC143C'
            }
        )
        fig_categoria.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig_categoria, use_container_width=True)
        
        # Tabela de análise detalhada por categoria
        st.subheader("🔍 Análise Detalhada por Categoria")
        analise_detalhada = df_resultado.groupby('main_category').agg({
            'classificacao': ['count', 'sum'],
            'price': ['mean', 'median', 'std']
        }).round(2)
        
        # Renomear colunas
        analise_detalhada.columns = ['Total Produtos', 'Produtos fora Padrão', 'Preço Médio', 'Preço Mediano', 'Desvio Padrão']
        analise_detalhada['% fora Padrão'] = (analise_detalhada['Produtos fora Padrão'] / analise_detalhada['Total Produtos'] * 100).round(1)
        analise_detalhada = analise_detalhada.sort_values('% fora Padrão', ascending=False)
        
        st.dataframe(analise_detalhada, use_container_width=True)
    
    # Análise por marca (se não filtrada)
    if marca_selecionada == 'Todas':
        st.subheader("🏷️ Produtos fora do Padrão por Marca")
        
        analise_marca = df_resultado.groupby(['brand', 'status_preco']).size().unstack(fill_value=0)
        
        if 'Preço fora do Padrão' in analise_marca.columns:
            # Pegar apenas as top 10 marcas com mais produtos fora do padrão
            top_marcas = analise_marca.sort_values('Preço fora do Padrão', ascending=False).head(10)
            
            fig_marca = px.bar(
                top_marcas.reset_index(), 
                x='brand', 
                y=['Preço Normal', 'Preço fora do Padrão'],
                title="Top 10 Marcas - Distribuição de Preços",
                labels={'brand': 'Marca', 'value': 'Quantidade de Produtos'},
                color_discrete_map={
                    'Preço Normal': '#2E8B57',
                    'Preço fora do Padrão': '#DC143C'
                }
            )
            fig_marca.update_layout(height=500, xaxis_tickangle=-45)
            st.plotly_chart(fig_marca, use_container_width=True)
    
    # Gráfico de pizza original (distribuição geral)
    st.subheader("📈 Distribuição Geral dos Preços")
    counts = df_resultado['status_preco'].value_counts()
    
    fig_pizza = px.pie(
        values=counts.values, 
        names=counts.index, 
        title="Distribuição da Classificação de Preços",
        color_discrete_map={
            'Preço Normal': '#2E8B57',
            'Preço fora do Padrão': '#DC143C'
        }
    )
    st.plotly_chart(fig_pizza, use_container_width=True)
    
    # Download dos dados analisados
    st.subheader("💾 Download dos Resultados")
    csv = df_resultado.to_csv(index=False)
    st.download_button(
        label="📥 Baixar Dados Analisados (CSV)",
        data=csv,
        file_name=f"analise_precos_{categoria_selecionada}_{marca_selecionada}.csv",
        mime="text/csv"
    )

else:
    # Mostrar informações iniciais
    st.info("👆 Clique em 'Analisar Preços' para gerar a análise dos produtos fora do padrão.")
    
    # Estatísticas básicas do dataset
    st.subheader("📋 Informações do Dataset")
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Total de Produtos", f"{len(df_filtrado):,}")
    with col_info2:
        st.metric("Categorias", len(df_filtrado['main_category'].unique()))
    with col_info3:
        st.metric("Marcas", len(df_filtrado['brand'].unique()))