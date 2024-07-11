<h1 align="center">PizzaBot en Colab</h1>
<h3 align="center">Proyecto Final | Desarrollo de Aplicaciones LLM con LangChain, LlamaIndex y OpenAI</h3>

<h3 align="center">Enunciado: </h3>

<p align="center">Realizar una aplicación de chatbot para tomar pedidos de una pizzería. El chatbot debe tomar los datos del menú y precios de un archivo externo (pdf, cvs, etc.) a través de la técnica RAG. El chatbot debe contar con una interfaz gráfica generada a través de Streamlit.
Puedes usar un documento de menú descargado de Internet, generado por vos, o por una IA.
Puedes utilizar el LLM que creas conveniente.
<br/>
Entregables:
Cuaderno de Colab en formato ipynb (no debes incluir tu API Key en el código).</p>


# Descripción del proyecto
## Rotiseria Don Claudio - Chatbot de Pedidos

Este proyecto es una aplicación de chatbot que permite a los usuarios hacer pedidos en la Rotiseria Don Claudio. La aplicación utiliza un archivo CSV que contiene el menú y precios, y recomienda bebidas basadas en las descripciones de los artículos del menú utilizando la API de OpenAI.

## Características

- **Búsqueda Fuzzy:** Busca artículos en el menú basándose en la similitud de las palabras.
- **Recomendación de Bebidas:** Utiliza la API de OpenAI para recomendar bebidas que acompañen los artículos del menú.
- **Interfaz de Usuario:** Utiliza Streamlit para una interfaz gráfica sencilla y fácil de usar.
- **Mostrar Menú Completo:** Opción para mostrar todo el menú cargado desde un archivo CSV.

## Requisitos

- Google Colab
- OpenAI API Key

## Instalación y Configuración

1. Abre Google Colab y crea un nuevo cuaderno.

2. Copia y pega el siguiente código en una celda del cuaderno:

    ```python
    !pip install streamlit pandas fuzzywuzzy
    !npm install localtunnel
    !pip install openai==0.28

    # Configuración de la key la API de OpenAI
    from google.colab import userdata
    OPEN_KEY = userdata.get('OPENAI_API_KEY')

    #Importar dependencias
    import pandas as pd
    import openai
    import streamlit as st
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process

    # Cargar el archivo CSV del menú
    menu = pd.read_csv('Menu.csv')

    #Importar la KEY
    openai.api_key = OPEN_KEY

    # Función para generar una respuesta basada en la entrada del usuario
    def generate_response(user_input, menu):
        # Buscar el artículo más similar en el menú
        result = process.extractOne(user_input, menu['item'], scorer=fuzz.partial_ratio)
        # Obtener el artículo del menú que coincide
        if result and result[1] > 50:
            menu_item = menu[menu['item'] == result[0]].iloc[0]
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
            max_tokens=60
        )
        return response.choices[0].text.strip()

    # Crear la aplicación Streamlit
    st.title('Rotiseria Don Claudio')
    user_input = st.text_input("¿Qué te gustaría comer hoy?:")

    if st.checkbox('Mostrar menú completo'):
        st.write(menu)

    if st.button('Enviar'):
        if user_input:
            response = generate_response(user_input, menu)
            st.write(response)
        else:
            st.write("Por favor, escribe algo en el campo de pedido.")

    # Guarda la celda anterior en un app.py y logs.txt
    !streamlit run /content/app.py &>/content/logs.txt &

    # La contraseña del tunel está en logs.txt, el número de "External URL" quitando el "http://"" y "":8501". Es decir la IP provista por Colab

    import subprocess
    # Inicia Streamlit en segundo plano
    process = subprocess.Popen(['streamlit', 'run', 'app.py'])

    !npx localtunnel --port 8501
    ```

3. Asegúrate de tener el archivo `Menu.csv` en tu Google Colab, que contenga los artículos del menú, precios y descripciones en el siguiente formato:
    ```csv
    item,price,description
    Pizza Margherita,8.50,Pizza con salsa de tomate, mozzarella y albahaca.
    Pizza Pepperoni,9.00,Pizza con salsa de tomate, mozzarella y pepperoni.
    ...
    ```

4. Coloca tu clave de API de OpenAI en Google Colab:
    - Ve a `Entorno de ejecución` > `Editar variables de entorno`.
    - Añade una variable `OPENAI_API_KEY` con tu clave de API de OpenAI.

5. Ejecuta todas las celdas en el cuaderno para instalar las dependencias y configurar el entorno.

6. Una vez ejecutadas todas las celdas, la aplicación Streamlit se ejecutará en segundo plano y se abrirá un túnel local usando localtunnel. La URL del túnel se mostrará en los logs.

## Uso

1. Accede a la URL proporcionada por localtunnel desde los logs de ejecución de Google Colab.
2. Interactúa con la aplicación ingresando tus pedidos y recibiendo recomendaciones de bebidas.

## Estructura del Proyecto

- `app.py`: Archivo principal que contiene la lógica del chatbot y la configuración de Streamlit.
- `Menu.csv`: Archivo CSV que contiene los artículos del menú, precios y descripciones.


## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Links
Link del menú .cvs: https://drive.google.com/file/d/1Z71WcpYjqGq9u7U82PVCe-r0aIaBdqQ9/view?usp=sharing
Link de colab: https://colab.research.google.com/drive/1V1Ve_NaMLSlMlhJraCRhGpQdPasd0kpd?usp=sharing