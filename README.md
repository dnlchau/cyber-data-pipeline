# CISA Known Exploited Vulnerabilities Pipeline

Pipeline de Engenharia de Dados para ingestão, transformação e visualização do catálogo **Known Exploited Vulnerabilities (KEV)** da CISA.

O projeto implementa uma arquitetura em camadas (**Raw → Bronze → Silver**) utilizando Python e Pandas, culminando em um dashboard interativo desenvolvido com Streamlit.

---

## Arquitetura

```text
              CISA KEV Catalog (JSON)
                       │
                       ▼
                 Raw (JSON)
                       │
                       ▼
             Bronze (Parquet)
                       │
                       ▼
             Silver (Parquet)
                       │
                       ▼
          Dashboard (Streamlit)
```

---

## Tecnologias

- Python 3
- Pandas
- Requests
- PyArrow
- Streamlit
- Plotly

---

## Estrutura do Projeto

```text
projeto/
│
├── data/
│   ├── raw/
│   │   └── kev.json
│   ├── bronze/
│   │   └── kev.parquet
│   └── silver/
│       └── kev.parquet
│
├── src/
│   ├── crawler/
│   │   └── kev_downloader.py
│   │
│   ├── bronze/
│   │   └── loader.py
│   │
│   ├── silver/
│   │   └── processor.py
│   │
│   └── dashboard.py
│
├── run.py
├── requirements.txt
└── README.md
```

---

## Pipeline

### 1. Raw

Baixa o catálogo oficial da CISA em formato JSON sem qualquer modificação.

### 2. Bronze

Converte o JSON para Parquet preservando praticamente toda a estrutura original.

### 3. Silver

Realiza o tratamento dos dados:

- remoção de registros duplicados
- limpeza de textos
- conversão de datas
- criação das colunas:
  - year
  - month
  - month_name
  - description_length
  - cwe_count
  - ransomware

---

## Como executar

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

### 2. Executar o pipeline

```bash
python run.py
```

O pipeline irá:

- baixar o catálogo oficial da CISA;
- salvar o JSON em `data/raw`;
- gerar o Parquet Bronze;
- gerar o Parquet Silver.

---

### 3. Executar o dashboard

```bash
python -m streamlit run dashboard.py
```

---

## Fonte dos dados

Os dados são obtidos do catálogo oficial **Known Exploited Vulnerabilities (KEV)**, mantido pela **Cybersecurity and Infrastructure Security Agency (CISA)**.

https://www.cisa.gov/known-exploited-vulnerabilities-catalog

---

## Análises disponíveis

O dashboard apresenta indicadores como:

- Total de CVEs
- Evolução mensal das vulnerabilidades
- Evolução anual
- Top fabricantes (Vendors)
- Top produtos afetados
- Vulnerabilidades relacionadas a campanhas de ransomware
- Busca por fabricante
- Busca por produto
- Busca por CVE
- Tabela detalhada das vulnerabilidades

---

## Licença

Este projeto utiliza dados públicos disponibilizados pela **Cybersecurity and Infrastructure Security Agency (CISA)**.
