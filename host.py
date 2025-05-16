import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import base64
import requests
import os
def set_bg_image(image_path):
    with open(image_path, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        h1 {{
            color: white !important;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)
set_bg_image('car_background.png')

file_id = "1f1cRNbKrnmse_GvnQkS6UYS61bRRcT_t" 
url = f"https://drive.google.com/uc?export=download&id={file_id}"
output_path = "car_price_model.pkl"

if not os.path.exists(output_path):
    response = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(response.content)

model=joblib.load('car_price_model.pkl')
marque_encoder=joblib.load('marque_encoder.pkl')
modele_encoder=joblib.load('modele_encoder.pkl')
carburant_encoder=joblib.load('carburant_encoder.pkl')
title = "<h1 style='text-align:center;color:white;'>Car Price Prediction</h1>"
st.markdown(title, unsafe_allow_html=True)
st.markdown("<p style='color:white;margin-bottom:1px;'><b>Marque/Brand</b></p>", unsafe_allow_html=True)
marque=st.text_input('','ex: Toyota').strip().lower()
st.markdown('</br>',unsafe_allow_html=True)
st.markdown("<p style='color:white;margin-bottom:1px;'><b>Modèle (2 mots max)/Model (2 words max)</b></p>",
             unsafe_allow_html=True)
modele=st.text_input('','ex: Corolla').strip().lower()
st.markdown('</br>',unsafe_allow_html=True)
st.markdown("<p style='color:white;margin-bottom:1px;'><b>Année/Year</b></p>", unsafe_allow_html=True)
annee=st.number_input("",min_value=1999,max_value=2025)
st.markdown('</br>',unsafe_allow_html=True)
st.markdown("<p style='color:white;margin-bottom:1px;'><b>Carburant/Fuel</b></p>", unsafe_allow_html=True)
carburant=st.selectbox("",['Diesel','Essence','Hybride','Electrique','LPG']).lower()
st.markdown('</br>',unsafe_allow_html=True)
st.markdown("<p style='color:white;margin-bottom:1px;'><b>Boîte/Gearbox</b></p>", unsafe_allow_html=True)
boite=st.selectbox("",['Manuelle','Automatique'])
st.markdown('</br></br>',unsafe_allow_html=True)

if st.button('Find Price Range'):
    try:
        marque_encoded=marque_encoder.transform([marque])[0]
        modele_encoded=float(modele_encoder.transform([modele]).sum(axis=1)[0])
        carburant_encoded=carburant_encoder.transform([carburant])[0]
        boite_encoded=1 if boite=='Automatique' else 0
        new=pd.DataFrame({
            'Marque_encoded':[marque_encoded],
            'Modèle_encoded':[modele_encoded],
            'Année':[annee],
            'Carburant_encoded':[carburant_encoded],
            'Boite_encoded':[boite_encoded]
            })
        result=model.predict(new)[0]
        if result<72346.24072281423:
            low=result
        else:
            low=result-72346.24072281423
        high=result+72346.24072281423

        st.markdown(f"<h2 style='color:white;'>Predicted price range: </h2>",unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:#d4edda;'><b>{int(low)} MAD - {int(high)} MAD</b></h2>",unsafe_allow_html=True)
    except Exception as e:
        st.error(f'error: {e}. must check your inputs')
