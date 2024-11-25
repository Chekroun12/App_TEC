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
        background-image: url('https://images.unsplash.com/photo-1606788075765-1f60e5b9a5cd');
        background-size: cover;
        background-attachment: fixed;
    }
    h1, h2, h3 {
        color: #007bff;
    }
    .stApp {
        background-color: rgba(244, 244, 244, 0.9);
        padding: 10px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #e9ecef;
        padding: 20px;
        border-radius: 10px;
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
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv'

# Fonction pour charger les données
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.replace('\xa0', ' ')
    return df

data = load_data(url)

# Menu pour naviguer entre les sections
menu = st.sidebar.selectbox("Menu", ["Vue d'ensemble", "Visualisations", "Statistiques descriptives"])

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
            fig1 = px.histogram(data, x='HEIGHT W/O SHOES', nbins=20, title="Distribution de la Taille des Joueurs", color_discrete_sequence=['#007bff'])
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.write("### Poids vs Taille")
        if 'HEIGHT W/O SHOES' in data.columns and 'WEIGHT (LBS)' in data.columns:
            fig2 = px.scatter(data, x='HEIGHT W/O SHOES', y='WEIGHT (LBS)', title="Relation entre Poids et Taille", color='POSITION')
            st.plotly_chart(fig2, use_container_width=True)

    # Nouveau graphique interactif
    st.write("### Moyenne des statistiques par Position")
    if 'POSITION' in data.columns and 'HEIGHT W/O SHOES' in data.columns:
        avg_stats = data.groupby('POSITION')[['HEIGHT W/O SHOES', 'WEIGHT (LBS)']].mean().reset_index()
        fig3 = px.bar(avg_stats, x='POSITION', y='HEIGHT W/O SHOES', title='Taille Moyenne par Position', color='POSITION')
        st.plotly_chart(fig3, use_container_width=True)

# Section 3 : Statistiques descriptives
elif menu == "Statistiques descriptives":
    st.title("Statistiques descriptives des données NBA Combine")
    st.write("### Statistiques générales")
    st.write(data.describe())

    # Distribution du Body Fat %
    st.write("### Distribution du Body Fat %")
    if 'BODY FAT %' in data.columns:
        fig4 = px.histogram(data, x='BODY FAT %', nbins=20, title="Distribution du Body Fat % des Joueurs", color_discrete_sequence=['#ff6347'])
        st.plotly_chart(fig4, use_container_width=True)
