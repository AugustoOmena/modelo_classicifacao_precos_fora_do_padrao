# Tech Challenge 3 (Fase 3): Aplicação Streamlit (Dashboard)

Este projeto apresenta um Dashboard interativo desenvolvido em **Streamlit** para visualização e interação com os modelos de Machine Learning construídos no contexto do Tech Challenge 3 da FIAP PosTech.

### Acesse a Aplicação

Você pode acessar a aplicação Streamlit diretamente através do seguinte link público:

[https://tech-challenge-3-grupo64.streamlit.app/](https://tech-challenge-3-grupo64.streamlit.app/)

## Funcionalidades



### Modelo 1 - Análise de Clientes

- Clusterização de clientes por comportamento
- Segmentação automática de perfis
- Análise de padrões de consumo
- Identificação de grupos similares

### Modelo 2 - Previsão de Probabilidade de Compra

- Predição de conversão de vendas
- Análise de sessões de clientes
- Insights por marca, categoria e período
- Dashboard com métricas de conversão

### Modelo 3 - Preços fora do Padrão

- Classificação de produtos com preços anômalos
- Análise por categoria e marca
- Identificação automática de outliers
- Visualizações interativas de pricing

## Tecnologias Utilizadas

- **Python 3.11** - Linguagem de programação
- **Streamlit** - Framework para interface web
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas
- **Scikit-learn** - Algoritmos de Machine Learning
- **Joblib** - Serialização de modelos

## Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

## Instalação e Execução

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

## Formato dos Dados

### Para Modelo 1:

```csv
["user_id", "total_spent", "frequency", "recency_days"]
```

### Para Modelo 2:
- Deve conter as **colunas já codificadas (numéricas)**.
  
```csv
["price", "brand_encoded", "main_category_encoded", "sub_category_encoded", "hour", "weekday_encoded", "add_to_cart_count", "views_count"]
```

### Para Modelo 3:

```csv
['price', 'price_ratio_cat', 'main_category', 'brand']
```

## Estrutura do Projeto

```
streamlitapp/
├── app.py                # Página inicial
├── utils.py              # Funções utilitárias
├── requirements.txt      # Dependências
├── .streamlit/
│   └── config.toml
├── pages/
│   ├── modelo_1.py      # Modelo 1 - Análise de Clientes
│   ├── modelo_2.py      # Modelo 2 - Previsão de Probabilidade de Compra
│   └── modelo_3.py      # Modelo 3 - Preços fora do Padrão
├── models/
│   ├── modelo_kmeans.pkl
│   ├── modelo_reglog.pkl
│   └── modelo_randomforest.pkl
├── encoders/
│   ├── le_brand.pkl
│   ├── le_main_category.pkl
│   └── le_weekday.pkl
├── .gitgnore
└── README.md
```

## Como Usar

1. **Navegue** pelo menu lateral para escolher o modelo desejado
2. **Faça upload** do seu arquivo CSV ou use os dados de exemplo
3. **Configure filtros** por categoria, marca ou outros parâmetros
4. **Execute a análise** clicando no botão correspondente
5. **Visualize** os resultados através de gráficos e métricas
6. **Exporte** os dados analisados em formato CSV

## ✒️ Autores

| Nome                            |   RM    | Link do GitHub                                      |
|---------------------------------|---------|-----------------------------------------------------|
| Ana Paula de Almeida            | 363602  | [GitHub](https://github.com/Ana9873P)               |
| Augusto do Nascimento Omena     | 363185  | [GitHub](https://github.com/AugustoOmena)           |
| Bruno Gabriel de Oliveira       | 361248  | [GitHub](https://github.com/brunogabrieldeoliveira) |
| José Walmir Gonçalves Duque     | 363196  | [GitHub](https://github.com/WALMIRDUQUE)            |
| Pedro Henrique da Costa Ulisses | 360864  | [GitHub](https://github.com/ordepzero)              |


## 📄 Licença

Este projeto está licenciado sob a Licença MIT.  
Consulte o arquivo [license](docs/license/license.txt)  para mais detalhes.
