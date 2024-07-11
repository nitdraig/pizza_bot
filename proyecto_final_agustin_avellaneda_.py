# Instalar dependencias
# Link del menú .cvs: https://drive.google.com/file/d/1Z71WcpYjqGq9u7U82PVCe-r0aIaBdqQ9/view?usp=sharing
# pip install streamlit pandas fuzzywuzzy
# npm install localtunnel
# pip install openai==0.28

# Configuración de la key la API de OpenAI
from google.colab import userdata

OPEN_KEY = userdata.get("OPENAI_API_KEY")

# Importar dependencias
import pandas as pd
import openai
import streamlit as st
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Cargar el archivo CSV del menú
menu = pd.read_csv("Menu.csv")

# Importar la KEY

openai.api_key = OPEN_KEY


# Función para generar una respuesta basada en la entrada del usuario
def generate_response(user_input, menu):
    # Buscar el artículo más similar en el menú
    result = process.extractOne(user_input, menu["item"], scorer=fuzz.partial_ratio)
    # Obtener el artículo del menú que coincide
    if result and result[1] > 50:

        menu_item = menu[menu["item"] == result[0]].iloc[0]
        response = f"Este es el artículo más similar que encontré en el menú:\n{menu_item['item']} - ${menu_item['price']}\n"
        response += f"Descripción: {menu_item['description']}\n\n"

        # Recomendación de una bebida para acompañar el menú
        beverage_recommendation = recommend_beverage(result[0])
        response += f"Recomendación de bebida:\n{beverage_recommendation}"
    else:
        # Recomendar una comida aleatoria si no se encuentra una coincidencia suficiente
        random_item = menu.sample().iloc[0]
        response = f"No encontré ese artículo en el menú, pero te puedo recomendar:\n{random_item['item']} - ${random_item['price']}\n"
        response += f"Descripción: {random_item['description']}"

    return response


# Función para recomendar una bebida usando OpenAI
def recommend_beverage(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Recomienda una bebida para acompañar el siguiente artículo del menú en no más de 60 tokens: {user_input}",
        max_tokens=60,
    )
    return response.choices[0].text.strip()


# Crear la aplicación Streamlit
st.title("Rotiseria Don Claudio")
user_input = st.text_input("¿Qué te gustaría comer hoy?:")

if st.checkbox("Mostrar menú completo"):
    st.write(menu)

if st.button("Enviar"):
    if user_input:
        response = generate_response(user_input, menu)
        st.write(response)
    else:
        st.write("Por favor, escribe algo en el campo de pedido.")

# Guarda la celda anterior en un app.py y logs.txt
# streamlit run /content/app.py &>/content/logs.txt &

# La contraseña del tunel está en logs.txt, el número de "External URL" quitando el "http://"" y "":8501". Es decir la IP provista por Colab

import subprocess

# Inicia Streamlit en segundo plano
process = subprocess.Popen(["streamlit", "run", "app.py"])

# npx localtunnel --port 8501
