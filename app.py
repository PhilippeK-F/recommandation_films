import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MultiLabelBinarizer
import base64

df = pd.read_csv("final_poster.csv")

titres_films = df['title']
titres_films =(titres_films).sort_values()


image = open("Fond.png", "rb").read()
encoded = base64.b64encode(image).decode()
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        backgroung-repeat:no-repeat
        background-position: bottom-center;
        color: #ff0033;  /* couleur du texte */
        font-family: 'Montserrat', sans-serif;
    }}

    /* Titre principal */
    h1, h2, h3 {{
        color: #ff0033;
        font-family: 'Bebas Neue', sans-serif;
        letter-spacing: 1px;
    }}

    /* Checkbox et texte */
    label, .css-17eq0hr, .css-10trblm {{
        color: #ff0033 !important;
    }}

    .stButton > button {{
        color: white;
        background-color: #ff0033;
        border: none;
        padding: 0.75em 1.5em;
        border-radius: 8px;
        font-weight: bold;
    }}
    .stButton > button:hover {{
        background-color: #ff0033;
        cursor: pointer;
    }}
    </style>
""", unsafe_allow_html=True)



#st.image("logo.png", width=150)


debut_lien='https://image.tmdb.org/t/p/w500/'

st.title("Bienvenue dans notre moteur de recherche!")

film_depart=st.selectbox("Selection d'un film",label_visibility='hidden',index=None,options= titres_films,placeholder="Sélectionne un film")
col1, col2 = st.columns(2)
with col1:
    checkbox_film=st.button("Informations sur le film")
with col2:
    checkbox_recommand=st.button("Films similaires")

if checkbox_film:
    fin_lien=df[df['title'] == film_depart]['poster_path'].values[0]
    lien=debut_lien+fin_lien
    st.image(lien)

    url_film = "https://www.allocine.fr/rechercher/?q={film_depart}"
    

    # st.markdown(f"""
    #     **Résumé du film** : {df[df['title'] == film_depart]['overview'].values[0]}    
    #     **Titre** : {film_depart}    
    #     **Année** : {df[df['title'] == film_depart]['release_date'].values[0]}    
    #     **Genres** : {df[df['title'] == film_depart]['genres'].values[0]}    
    #     **Note** : {df[df['title'] == film_depart]['averageRating'].values[0]}    
    #     **Bande-annonce**:[Voir la vidéo] ({url_film})
    #     """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        background-color: rgba(0, 0, 0, 0.85);  /* fond noir semi-transparent */
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        font-size: 16px;
        line-height: 1.6;
        width: 90%;
        margin: auto;
        text-shadow: 1px 1px 2px black;
        font-family: 'Montserrat', sans-serif;
    ">
    <b>Résumé du film</b> : {df[df['title'] == film_depart]['overview'].values[0]}<br>
    <b>Titre</b> : {film_depart}<br>
    <b>Année</b> : {df[df['title'] == film_depart]['release_date'].values[0]}<br>
    <b>Genres</b> : {df[df['title'] == film_depart]['genres'].values[0]}<br>
    <b>Note</b> : {df[df['title'] == film_depart]['averageRating'].values[0]} /10<br>
    <b>Bande-annonce</b> : <a href="{url_film}" target="_blank" style="color:#FF4081;">Voir la vidéo</a>
    </div>
    """, unsafe_allow_html=True)


if checkbox_recommand:
    cols = ["genres", "actor_or_actress","director","producer"]
    for col in cols:
        df[col] = df[col].fillna("[]")

    df["release_date"] = df["release_date"].replace("[]", "0000")
    df["release_date"] = df["release_date"].fillna("0000")
    df["release_date"] = df["release_date"].astype(str).str[:4]
    df["release_date"] = df["release_date"].astype(int)

    k=6

    encoder_genres = MultiLabelBinarizer()
    X_genres = encoder_genres.fit_transform(df["genres"])

    encoder_actors = MultiLabelBinarizer()
    X_actors = encoder_actors.fit_transform(df["actor_or_actress"])

    encoder_actors = MultiLabelBinarizer()
    X_director = encoder_actors.fit_transform(df["director"])

    encoder_actors = MultiLabelBinarizer()
    X_producer = encoder_actors.fit_transform(df["producer"])

    X_date = df[["release_date"]].values


    X_tot = np.hstack([X_genres, X_actors,X_director, X_producer, X_date])
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(X_tot)

    idx = df[df["title"] == film_depart].index[0]
    distances, indices = knn.kneighbors([X_tot[idx]])

    for i in indices[0][1:]:
        #print("-", df.iloc[i]["title"])
        fin_lien=df[df['title'] == df.iloc[i]["title"]]['poster_path'].values[0]
        lien=debut_lien+fin_lien
        st.image(lien)


