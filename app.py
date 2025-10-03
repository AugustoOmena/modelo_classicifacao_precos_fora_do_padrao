import streamlit as st

st.set_page_config(
    page_title="Análise de Preços",
    page_icon=":material/analytics:",
    layout="wide"
)

st.markdown('<h1 style="color:#1a73e8;">Sistema de Análise de Preços</h1>', unsafe_allow_html=True)

st.markdown("""
## Sobre o Projeto

Este projeto foi desenvolvido para identificar **produtos com preços fora do padrão** utilizando técnicas de Machine Learning. 
O sistema oferece diferentes modelos analíticos para apoiar decisões de pricing e estratégias comerciais.

### :material/target: Modelos Disponíveis

**:material/trending_up: Modelo 1 - Classificação**
- Identifica produtos com preços anômalos
- Análise por categoria e marca
- Visualizações interativas
- Métricas de performance
- Export de resultados

**:material/donut_small: Modelo 2 - Clusterização**  
- Segmentação de clientes
- Análise de comportamento de consumo
- Identificação de grupos similares

### :material/lightbulb: Como Funciona

O sistema utiliza algoritmos de **Regressão Logística** treinados com dados históricos de preços, 
categorizando produtos como "Preço Normal" ou "Preço fora do Padrão" com base em:

- Preço do produto
- Razão de preço por categoria
- Categoria principal
- Marca

### :material/checklist: Como Usar

1. **Navegue** pelo menu lateral para escolher o modelo
2. **Faça upload** do seu CSV ou use os dados de exemplo
3. **Configure filtros** por categoria ou marca
4. **Execute a análise** e visualize os resultados
5. **Exporte** os dados analisados

---
**:material/lightbulb: Selecione um modelo no menu lateral para começar a análise!**
""")

# Informações técnicas
with st.expander(":material/info: Informações Técnicas"):
    st.markdown("""
    **Tecnologias Utilizadas:**
    - Python 3.11
    - Streamlit (Interface)
    - Pandas (Manipulação de dados)
    - Plotly (Visualizações)
    - Scikit-learn (Machine Learning)
    
    **Requisitos dos Dados:**
    - Formato: CSV
    - Colunas obrigatórias: `price`, `price_ratio_cat`, `main_category`, `brand`
    - Encoding: UTF-8
    """)