import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Mini-Site NBA Combine", page_icon="🏀", layout="wide")

# CSS intégré (identique à votre code précédent)
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

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
            fig1 = px.histogram(data, x='HEIGHT W/O SHOES', nbins=20, title="Distribution de la Taille des Joueurs")
            st.plotly_chart(fig1)

    with col2:
        st.write("### Poids vs Taille")
        if 'HEIGHT W/O SHOES' in data.columns and 'WEIGHT (LBS)' in data.columns:
            fig2 = px.scatter(data, x='HEIGHT W/O SHOES', y='WEIGHT (LBS)', title="Relation entre Poids et Taille")
            st.plotly_chart(fig2)
    
    # Slider for interactive height filter
    st.write("### Filtrer par Taille des Joueurs")
    if 'HEIGHT W/O SHOES' in data.columns:
        min_height = int(data['HEIGHT W/O SHOES'].min())
        max_height = int(data['HEIGHT W/O SHOES'].max())
        
        # Slider for height range selection
        height_range = st.slider("Sélectionnez une plage de taille (en inches):", min_value=min_height, 
                                 max_value=max_height, value=(min_height, max_height))
        
        # Filter data based on slider selection
        filtered_data = data[(data['HEIGHT W/O SHOES'] >= height_range[0]) & 
                             (data['HEIGHT W/O SHOES'] <= height_range[1])]
        
        # Scatter plot with filtered data
        fig_slider = px.scatter(filtered_data, x='HEIGHT W/O SHOES', y='WEIGHT (LBS)', 
                                title=f"Poids vs Taille pour la Plage Sélectionnée ({height_range[0]}-{height_range[1]} inches)")
        st.plotly_chart(fig_slider)

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
