import pandas as pd
import streamlit as st
import plotly.express as px

# =====================================================
# Configuração
# =====================================================

st.set_page_config(
    page_title="CISA KEV Dashboard",
    layout="wide"
)

st.title("🛡️ CISA Known Exploited Vulnerabilities Dashboard")

# =====================================================
# Carrega dados
# =====================================================

df = pd.read_parquet("data/silver/kev.parquet")

# =====================================================
# Sidebar
# =====================================================

st.sidebar.header("Filtros")

anos = sorted(df["year"].unique())

ano = st.sidebar.selectbox(
    "Ano",
    ["Todos"] + anos
)

vendors = sorted(df["vendorProject"].dropna().unique())

vendor = st.sidebar.selectbox(
    "Vendor",
    ["Todos"] + vendors
)

texto = st.sidebar.text_input(
    "Pesquisar CVE"
)

# =====================================================
# Filtros
# =====================================================

if ano != "Todos":
    df = df[df["year"] == ano]

if vendor != "Todos":
    df = df[df["vendorProject"] == vendor]

if texto:
    df = df[
        df["cveID"].str.contains(
            texto,
            case=False,
            na=False
        )
    ]

# =====================================================
# KPIs
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total CVEs",
    len(df)
)

col2.metric(
    "Vendors",
    df["vendorProject"].nunique()
)

col3.metric(
    "Produtos",
    df["product"].nunique()
)

col4.metric(
    "Ransomware",
    int(df["ransomware"].sum())
)

st.divider()

# =====================================================
# CVEs por mês
# =====================================================

st.subheader("CVEs adicionadas por mês")

monthly = (
    df.groupby(["year", "month"])
      .size()
      .reset_index(name="CVEs")
)

monthly["Data"] = pd.to_datetime(
    monthly["year"].astype(str)
    + "-"
    + monthly["month"].astype(str)
)

fig = px.bar(
    monthly,
    x="Data",
    y="CVEs",
    title="Quantidade de CVEs por mês"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Top Vendors
# =====================================================

st.subheader("Top 10 Vendors")

top_vendor = (
    df["vendorProject"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_vendor.columns = [
    "Vendor",
    "CVEs"
]

fig = px.bar(
    top_vendor,
    x="Vendor",
    y="CVEs",
    title="Top 10 Vendors"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Top Produtos
# =====================================================

st.subheader("Top 10 Produtos")

top_product = (
    df["product"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_product.columns = [
    "Produto",
    "CVEs"
]

fig = px.bar(
    top_product,
    x="Produto",
    y="CVEs",
    title="Top 10 Produtos"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Ransomware
# =====================================================

st.subheader("Campanhas de Ransomware")

ransom = (
    df["ransomware"]
    .value_counts()
    .rename_axis("Ransomware")
    .reset_index(name="Quantidade")
)

fig = px.pie(
    ransom,
    names="Ransomware",
    values="Quantidade",
    title="CVEs relacionadas a ransomware"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Tabela
# =====================================================

st.subheader("Detalhamento")

st.dataframe(
    df[
        [
            "cveID",
            "vendorProject",
            "product",
            "vulnerabilityName",
            "dateAdded",
            "ransomware"
        ]
    ],
    use_container_width=True
)