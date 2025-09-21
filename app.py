import streamlit as st
from models import model_1
from utils.display import exibir_painel_de_resultado

# --- Configuração da página ---
st.set_page_config(
    page_title="Tech Challenger 3",
    page_icon="📊",
    layout="wide"
)

# --- Carregar modelo ---
model = model_1.load_model()

# --- Layout principal ---
left_col, spacer, right_col = st.columns([1.2, 0.2, 1])

with left_col:
    st.markdown('<h1 style="color:#1a73e8;">Modelo 1 - Classificação - Preços fora do Padrão</h1>', unsafe_allow_html=True)

    st.markdown("""
    **Preço (price):** Insira o valor do produto que você quer verificar.  
    **Relação de Preço (price_ratio_cat):** Este campo é crucial para o modelo.  

    - Um valor como `1.5` significa que o preço atual é **50% maior** que o preço médio.  
    - Um valor como `0.8` significa que o preço atual é **20% menor** que o preço médio.  

    O modelo usa essa informação para entender se o preço está fora do padrão,
    independentemente do valor absoluto.
    """)

    # Inputs
    c1, c2 = st.columns(2)
    with c1:
        feature_1 = st.number_input("Preço", min_value=0.0, max_value=10000.0, value=735.0, step=0.1)
    with c2:
        feature_2 = st.number_input("Relação de Preço", min_value=0.0, max_value=100.0, value=1.48, step=0.1)

    gerar = st.button("🚀 Classificar", type="primary", use_container_width=True)

with right_col:
    st.markdown('<div style="margin-top:50px;"></div>', unsafe_allow_html=True)

    class_text_result = "Ainda não classificado"
    confidence_result = None
    color_result = None

    if gerar:
        if model:
            try:
                prediction, confidence_result = model_1.predict(model, [feature_1, feature_2])
                if prediction == 1:
                    class_text_result = "🔴 Preço fora do padrão"
                    color_result = "#e53935"
                else:
                    class_text_result = "✅ Preço normal"
                    color_result = "#43a047"
            except Exception as e:
                st.error(f"Erro durante a previsão: {e}")
                class_text_result = "Erro na classificação"
        else:
            st.warning("⚠️ O modelo não pôde ser carregado.")

    exibir_painel_de_resultado(class_text_result, confidence_result, color_result)
