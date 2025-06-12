import streamlit as st
import pandas as pd

# # Titre principal de l'application (affiché en haut de la page)
# st.title("The title of my page")

# # Titre de section important (taille 1)
# st.header("An Important Header")

# # Sous-titre (taille 2), utile pour organiser le contenu par sous-sections
# st.subheader("A Secondary Header")

# # Affiche une ligne de texte simple (sans mise en forme particulière)
# st.text("My classic text")

# # Affiche du texte avec mise en forme Markdown
# st.markdown(''':rainbow: :rainbow[My markdown]''')  # Ici, un effet arc-en-ciel est appliqué

# # Affiche un dataframe (st.write accepte plusieurs arguments et plusieurs types de données)
# st.write(
#     pd.DataFrame({
#             "Cards": ['Name 1', 'Name 2', 'Name 3', 'Name 4'],
#             "Quantity": [0, 1, 0, 3]}
#     )
# )

df = pd.read_csv("final_poster.csv")

titres_films = df['title']
titres_films =(titres_films).sort_values()

debut_lien='https://image.tmdb.org/t/p/w500/'

st.title("Bienvenue dans notre moteur de recherche!")

film_depart=st.selectbox("Selectionne un film que tu as aimé", titres_films)
col1, col2 = st.columns(2)
with col1:
    checkbox_film=st.checkbox("Informations sur le film")
with col2:
    checkbox_recommand=st.checkbox("Films similaires")

if checkbox_film:
    fin_lien=df[df['title'] == film_depart]['poster_path'].values[0]
    lien=debut_lien+fin_lien
    st.image(lien)



    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{lien}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.5);  /* Ajuste ici pour plus ou moins de transparence */
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    
    
    st.markdown(f"""
        <div style="background-color: rgba(255, 255, 255, 0.7)
                    ; padding: 1rem; border-radius: 10px;">
    
        **Résumé du film** : {df[df['title'] == film_depart]['overview'].values[0]}  
        **Titre** : {film_depart}  
        **Année** : {df[df['title'] == film_depart]['release_date'].values[0]}  
        **Genres** : {df[df['title'] == film_depart]['genres'].values[0]}  
        **Note** : {df[df['title'] == film_depart]['averageRating'].values[0]}  

        </div>
        """, unsafe_allow_html=True)





