import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Mini-Site NBA Combine", page_icon="🏀", layout="wide")

# CSS intégré
st.markdown("""
    <style>
    body {
        font-family: sans-serif;
        background-color: #f4f4f4;
        color: #333;
        margin: 0;
        padding: 0;
    }
    h1, h2, h3 {
        color: #007bff;
    }
    .stApp {
        background-color: #f4f4f4;
    }
    .sidebar .sidebar-content {
        background-color: #e9ecef;
        padding: 20px;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
    .plotly-graph-div {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        margin-bottom: 20px;
    }
    h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        text-align: center;
    }
    h2 {
        margin-top: 30px;
        margin-bottom: 15px;
    }
    section {
        padding: 20px;
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
menu = st.sidebar.selectbox("Menu", ["Vue d'ensemble", "Visualisations", "Statistiques descriptives", "Analyses Avancées"])

# Section 1 : Vue d'ensemble
if menu == "Vue d'ensemble":
    st.title("Vue d'ensemble des données NBA Combine")
    st.write("### Aperçu des données")
    st.write(data.head())
    st.write("### Noms des colonnes")
    st.write(data.columns)

# Section 2 : Visualisations
elif menu == "Visualisations":
    st.title("Visualisations des données")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Distribution de la Taille (Inches)")
        if 'HEIGHT W/O SHOES' in data.columns:
            fig1 = px.histogram(data, x='HEIGHT W/O SHOES', nbins=20, title="Distribution de la Taille des Joueurs")
            st.plotly_chart(fig1)

    with col2:
        st.write("### Poids vs Taille")
        if 'HEIGHT W/O SHOES' in data.columns and 'WEIGHT (LBS)' in data.columns:
            fig2 = px.scatter(data, x='HEIGHT W/O SHOES', y='WEIGHT (LBS)', title="Relation entre Poids et Taille")
            st.plotly_chart(fig2)

# Section 3 : Statistiques descriptives
elif menu == "Statistiques descriptives":
    st.title("Statistiques descriptives des données NBA Combine")
    st.write("### Statistiques générales")
    st.write(data.describe())

    # Distribution du Body Fat %
    st.write("### Distribution du Body Fat %")
    if 'BODY FAT %' in data.columns:
        fig3 = px.histogram(data, x='BODY FAT %', nbins=20, title="Distribution du Body Fat % des Joueurs")
        st.plotly_chart(fig3)

# Nouvelle Section : Analyses Avancées
elif menu == "Analyses Avancées":
    st.title("Analyses Avancées des Joueurs NBA")

    col1, col2 = st.columns(2)
    with col1:
        st.write("### Distribution de la Taille (Inches)")
        if 'Height (Inches)' in data.columns:
            fig1 = px.histogram(data, x='Height (Inches)', nbins=20, title="Distribution de la Taille des Joueurs")
            st.plotly_chart(fig1)
        else:
            st.warning("La colonne 'Height (Inches)' n'est pas présente dans le dataset.")

    with col2:
        st.write("### Poids vs Taille")
        if 'Height (Inches)' in data.columns and 'Weight (LBS)' in data.columns:
            fig2 = px.scatter(data, x='Height (Inches)', y='Weight (LBS)', title="Relation entre Poids et Taille")
            st.plotly_chart(fig2)
        else:
            st.warning("Les colonnes 'Height (Inches)' et/ou 'Weight (LBS)' ne sont pas présentes dans le dataset.")

    col3, col4 = st.columns(2)
    with col3:
        st.write("### Boxplot de la Taille par Année de Draft")
        if 'Draft Year' in data.columns and 'Height (Inches)' in data.columns:
            fig3 = px.box(data, x='Draft Year', y='Height (Inches)', title="Distribution de la Taille par Année de Draft")
            st.plotly_chart(fig3)
        else:
            st.warning("Les colonnes 'Draft Year' et/ou 'Height (Inches)' ne sont pas présentes dans le dataset.")

    with col4:
        st.write("### Répartition des Positions")
        if 'Position' in data.columns:
            position_counts = data['Position'].value_counts().reset_index()
            position_counts.columns = ['Position', 'Nombre']
            fig4 = px.pie(position_counts, values='Nombre', names='Position', title="Répartition des Positions des Joueurs")
            st.plotly_chart(fig4)
        else:
            st.warning("La colonne 'Position' n'est pas présente dans le dataset.")
