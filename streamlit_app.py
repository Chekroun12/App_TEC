import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Mini-Site NBA Combine", page_icon="🏀", layout="wide")

# CSS intégré avec thème professionnel
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f9f9f9;
        color: #333333;
    }
    .stApp {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #f1f1f1;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #004080;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #004080;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00264d;
    }
    .plotly-graph-div {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    th, td {
        border: 1px solid #dddddd;
        padding: 10px;
        text-align: center;
    }
    th {
        background-color: #004080;
        color: white;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    section {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# URL du fichier Google Sheets en format CSV
gsheetid = "1BM2uotZg84vpEcyHJcoC-6uw6nJGwByImclWzX94MRo"
sheetid = "1755484415"
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv'

# Fonction pour charger les données
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.replace('\xa0', ' ')
    return df

data = load_data(url)

# Menu pour naviguer entre les sections
menu = st.sidebar.selectbox("🏀 Menu", ["Vue d'ensemble", "Visualisations", "Statistiques descriptives"])

# Section 1 : Vue d'ensemble
if menu == "Vue d'ensemble":
    st.title("🏀 Vue d'ensemble des données NBA Combine")
    st.write("### Aperçu des données")
    st.write(data.head())
    st.write("### Noms des colonnes")
    st.write(data.columns)

# Section 2 : Visualisations
elif menu == "Visualisations":
    st.title("📊 Visualisations des données")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 🏀 Distribution de la Taille (Inches)")
        if 'HEIGHT W/O SHOES' in data.columns:
            fig1 = px.histogram(data, x='HEIGHT W/O SHOES', nbins=20, title="Distribution de la Taille des Joueurs")
            st.plotly_chart(fig1)

    with col2:
        st.write("### 💪 Poids vs Taille")
        if 'HEIGHT W/O SHOES' in data.columns and 'WEIGHT (LBS)' in data.columns:
            fig2 = px.scatter(data, x='HEIGHT W/O SHOES', y='WEIGHT (LBS)', title="Relation entre Poids et Taille")
            st.plotly_chart(fig2)

# Section 3 : Statistiques descriptives
elif menu == "Statistiques descriptives":
    st.title("📈 Statistiques descriptives des données NBA Combine")
    st.write("### 📊 Statistiques générales")
    st.write(data.describe())

    st.write("### 🏃‍♂️ Distribution du Body Fat %")
    if 'BODY FAT %' in data.columns:
        fig3 = px.histogram(data, x='BODY FAT %', nbins=20, title="Distribution du Body Fat % des Joueurs")
        st.plotly_chart(fig3)
