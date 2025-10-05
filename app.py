import streamlit as st

st.set_page_config(
    page_title="Tech Challenge 03 - ML Analytics",
    page_icon=":material/analytics:",
    layout="wide"
)

st.markdown('<h1 style="color:#1a73e8;">Tech Challenge 03 - Machine Learning Analytics</h1>', unsafe_allow_html=True)

st.markdown("""
## :material/target: Bem-vindo ao Sistema de Análise Preditiva

Este sistema utiliza **Machine Learning** para análise de dados de e-commerce, oferecendo insights valiosos 
para decisões estratégicas de negócio.

### :material/psychology: Modelos Disponíveis

**:material/groups: Modelo 1 - Análise de Clientes**
- Clusterização de clientes por comportamento
- Segmentação automática de perfis
- Análise de padrões de consumo
- Identificação de grupos similares

**:material/shopping_cart: Modelo 2 - Previsão de Probabilidade de Compra**
- Predição de conversão de vendas
- Análise de sessões de clientes
- Insights por marca, categoria e período
- Dashboard com métricas de conversão

**:material/price_check: Modelo 3 - Preços fora do Padrão (Bônus)**
- Classificação de produtos com preços anômalos
- Análise por categoria e marca
- Identificação automática de outliers
- Visualizações interativas de pricing

### :material/rocket_launch: Como Começar

1. :material/menu: **Navegue** pelo menu lateral
2. :material/upload: **Carregue** seus dados ou use os exemplos
3. :material/play_arrow: **Execute** a análise desejada
4. :material/insights: **Explore** os resultados e insights
5. :material/download: **Exporte** os dados processados

---

:material/arrow_forward: **Selecione um modelo no menu lateral para iniciar sua análise!**
""")