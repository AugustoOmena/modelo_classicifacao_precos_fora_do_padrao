# 📊 Tech Challenge 03 - Análise de Preços com Streamlit

Uma aplicação web interativa desenvolvida em Streamlit para análise e classificação de preços de produtos utilizando técnicas de Machine Learning.

## 🎯 Sobre o Projeto

Este sistema foi desenvolvido para identificar **produtos com preços fora do padrão** e realizar análises preditivas sobre comportamento de compra, oferecendo insights valiosos para decisões de pricing e estratégias comerciais.

## 🚀 Funcionalidades

### 📈 Modelo 1 - Classificação de Preços Anômalos

- Identifica produtos com preços fora do padrão
- Análise detalhada por categoria e marca
- Visualizações interativas com gráficos
- Métricas de performance em tempo real
- Export de resultados em CSV

### 🎯 Modelo 2 - Previsão de Probabilidade de Compra

- Predição de conversão de vendas
- Análise de sessões de clientes
- Identificação de potenciais compradores
- Insights por marca, categoria e dia da semana
- Dashboard com métricas consolidadas

### 🔍 Modelo 3 - Classificação K-Means

- Clustering de produtos por características de preço
- Segmentação automática
- Análise comparativa entre grupos
- Identificação de padrões de pricing

## 🛠️ Tecnologias Utilizadas

- **Python 3.11** - Linguagem de programação
- **Streamlit** - Framework para interface web
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas
- **Scikit-learn** - Algoritmos de Machine Learning
- **Joblib** - Serialização de modelos

## 📋 Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

## ⚡ Instalação e Execução

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Grupo-61/techchallenge03
   cd techchallenge03/streamlitapp
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**

   ```bash
   streamlit run app.py
   ```

4. **Acesse no navegador:**
   ```
   http://localhost:8501
   ```

## 📊 Formato dos Dados

### Para Modelo 1 e 3:

```csv
price,price_ratio_cat,main_category,brand
199.99,1.2,Electronics,Samsung
89.50,0.8,Clothing,Nike
```

### Para Modelo 2:

```csv
price,brand_encoded,main_category_encoded,sub_category_encoded,hour,weekday_encoded,add_to_cart_count,views_count
238.55,2653,5,119,0,2,0,98
150.00,10,5,120,14,5,2,15
```

## 📁 Estrutura do Projeto

```
streamlitapp/
├── app.py                 # Página principal
├── utils.py              # Funções utilitárias
├── requirements.txt      # Dependências
├── pages/
│   ├── modelo_2.py      # Modelo de previsão de compra
│   └── modelo_3.py      # Modelo de clustering
├── models/
│   └── modelo_randomforest.pkl
├── encoders/
│   ├── le_brand.pkl
│   ├── le_main_category.pkl
│   └── le_weekday.pkl
└── README.md
```

## 🎮 Como Usar

1. **Navegue** pelo menu lateral para escolher o modelo desejado
2. **Faça upload** do seu arquivo CSV ou use os dados de exemplo
3. **Configure filtros** por categoria, marca ou outros parâmetros
4. **Execute a análise** clicando no botão correspondente
5. **Visualize** os resultados através de gráficos e métricas
6. **Exporte** os dados analisados em formato CSV

## 📈 Exemplos de Uso

### Análise de Preços Anômalos

- Identifique produtos com preços muito acima ou abaixo da média
- Analise padrões por categoria de produto
- Compare performance entre marcas

### Previsão de Conversão

- Preveja quais sessões têm maior probabilidade de conversão
- Otimize campanhas de marketing
- Identifique os melhores dias para promoções

### Segmentação de Produtos

- Agrupe produtos com características similares
- Identifique oportunidades de pricing
- Analise distribuição de preços por cluster

## 🔧 Solução de Problemas

### Erro de carregamento de modelo

Se encontrar erros relacionados ao scikit-learn:

```bash
pip install scikit-learn
```

### Problemas com dependências

Reinstale todas as dependências:

```bash
pip install -r requirements.txt --upgrade
```

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte do Tech Challenge 03.

## 👥 Contribuição

Projeto desenvolvido pela equipe do Tech Challenge 03 da FIAP.

---

**💡 Dica:** Para melhor experiência, use navegadores modernos e mantenha a janela em tela cheia para visualizar todos os gráficos adequadamente.
