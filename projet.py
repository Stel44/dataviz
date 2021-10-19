import streamlit as st
import numpy as np
import pandas as pd 
import time
import matplotlib.pyplot as plt

def log(func):
    def wrapper(*args,**kwargs):
        with open("log.txt","a") as f:
            debut = time.time()
            value = func(*args,**kwargs)
            fin = time.time()
            f.write("\nCalled function "+ func.__name__ + " in "+ str(fin - debut)+"\n")
            return value
    return wrapper



st.title("Analyse de l'immobiler français sur les 2 dernières années")


@log
@st.cache(allow_output_mutation=True)
def load_dataset_20():
    df = pd.read_csv("full_2020.csv")
    df['adresse_code_voie'] = df['adresse_code_voie'].astype(str)
    df['code_commune'] = df['code_commune'].astype(str)
    df['code_departement'] = df['code_departement'].astype(str)
    df['numero_volume'] = df['numero_volume'].astype(str)
    df.drop(["lot1_numero", "lot2_numero", "lot3_numero", "lot4_numero", "lot5_numero", "lot1_surface_carrez", "lot2_surface_carrez", "lot3_surface_carrez", "lot4_surface_carrez", "lot5_surface_carrez", "adresse_suffixe", "ancien_nom_commune", "ancien_code_commune", "ancien_id_parcelle", "code_nature_culture", "nature_culture_speciale", "code_nature_culture_speciale", "numero_volume"], axis=1 , inplace=True)
    df['prix_par_metre_carre'] = df['valeur_fonciere'] / df['surface_terrain']
    return df

@log
@st.cache(allow_output_mutation=True)
def load_dataset_19():
    df = pd.read_csv("full_2019.csv")
    df['adresse_code_voie'] = df['adresse_code_voie'].astype(str)
    df['code_commune'] = df['code_commune'].astype(str)
    df['code_departement'] = df['code_departement'].astype(str)
    df['numero_volume'] = df['numero_volume'].astype(str)
    df.drop(["lot1_numero", "lot2_numero", "lot3_numero", "lot4_numero", "lot5_numero", "lot1_surface_carrez", "lot2_surface_carrez", "lot3_surface_carrez", "lot4_surface_carrez", "lot5_surface_carrez", "adresse_suffixe", "ancien_nom_commune", "ancien_code_commune", "ancien_id_parcelle", "code_nature_culture", "nature_culture_speciale", "code_nature_culture_speciale", "numero_volume"], axis=1 , inplace=True)
    df['prix_par_metre_carre'] = df['valeur_fonciere'] / df['surface_terrain']
    return df

def my_sidebar():
    st.sidebar.title("Options")

@log
def get_int(dt):
    if dt =="NaN":
        dt.dropna(subset = ["longitude"], inplace=True)
        dt.dropna(subset = ["latitude"], inplace=True)
    else:
        return dt

@log
def pie_chart(df):
    if st.sidebar.checkbox("Pie chart : Repartition Type local"):
        gb = df.groupby(['type_local'])
        by_type_local = gb.apply(count_rows).rename("nb_by_type_local")
        st.write(by_type_local)
        myexplode = [0, 0, 0, 0.2]
        plt.subplot()
        plt.pie(by_type_local, labels = ("Appartement", "Dependance", "Local industriel. commercial ou assimilé", "Maison"), explode = myexplode, shadow = True)
        plt.title('Répartition des types de local en 2020')
        st.pyplot(fig=plt)

@log
def bar_chart(df,df2):
    st.subheader("Prix moyen en fonction du type de local")
    gb = df.groupby(['type_local'])
    gb_2019 = df2.groupby(['type_local'])
    by_type_local = gb.apply(count_rows).rename("nb_by_type_local")
    by_type_price_2020 = gb.prix_par_metre_carre.mean().rename("moy_prix_metre_carre_2020")
    by_type_price_2019 = gb_2019.prix_par_metre_carre.mean().rename("moy_prix_metre_carre_2019")
    df4 = pd.merge(by_type_price_2020,by_type_price_2019, left_index=True, right_index=True)
    st.write(df4)
    chart_data = df4[["moy_prix_metre_carre_2020", "moy_prix_metre_carre_2019"]]
    st.bar_chart(chart_data)

@log
def display_table(df, text):
    if st.checkbox(text):
        st.subheader('Raw data')
        st.write(df)

@log
def count_rows(rows): 
    return len(rows)

@log
def prix_square_metter_rows(rows): 
    return np.mean(rows)

@log
def display_histo_one(df):
    if st.sidebar.checkbox("Histogramme : Transaction immobilière par department"):
        by_departement = df.groupby('code_departement').apply(count_rows)
        st.subheader('Nombre de transactions immobilière par depatement (Top 15) -- France _ 2020')
        plt.bar(range(1, 16), by_departement.nlargest(15))
        plt.xticks(range(1, 16), by_departement.nlargest(15).index)
        plt.xlabel('Departement')
        plt.ylabel('Nombre de transactions immobilière')
        st.pyplot(fig=plt)

@log
def MapFigure(df):
    df.dropna(subset = ["latitude"], inplace=True)
    df.dropna(subset = ["longitude"], inplace=True)
    surface_to_filter = st.sidebar.slider('Surface du bien : ', 9, 300, 95)
    type_to_filter = st.sidebar.selectbox("Choisissez un type de bien :", ["Maison", "Appartement", "Local industriel. commercial ou assimilé" ])
    filtered_data = df[(df["surface_reelle_bati"] == surface_to_filter) & (df["type_local"] == type_to_filter)]
    st.subheader('Situation géographique des %ss de %s mètre carré en France' % (type_to_filter, surface_to_filter))
    st.map(filtered_data)

def main():    
    
    st.markdown('### Le Masne de Chermont Armel- Projet')

    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

    option = st.sidebar.selectbox(
        'Quel dataset voulez-vous afficher ?',
        ('Data 2020', 'Data 2019'))

    # 2020
    if option == 'Data 2020':
        my_sidebar()
        df_2020 = load_dataset_20()
        df_2020_sample = df_2020.sample(n=10, random_state=1)
        display_table(df_2020_sample, "Voir un echantillons du data set 2020")
                    
        st.title("2020")
        MapFigure(df_2020)

        st.sidebar.text("Autres visualisations")
        display_histo_one(df_2020)
        pie_chart(df_2020)

    # 2019
    else : 
        my_sidebar()
        df_2019 = load_dataset_19()
        df_2019_sample = df_2019.sample(n=10, random_state=1)
        display_table(df_2019_sample, "Voir un echantillons du data set 2019")
                    
        st.title("2019")
        MapFigure(df_2019)    
    
        st.sidebar.text("Autres visualisations")
        display_histo_one(df_2019)
        
        pie_chart(df_2019)

if __name__=="__main__":
    main()