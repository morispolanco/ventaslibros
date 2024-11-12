import streamlit as st
import requests
import numpy as np

# Obtén la API Key desde los Secrets de Streamlit
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

# Función para obtener datos del libro en Amazon usando Serper
def get_amazon_data(keyword):
    url = 'https://api.serper.dev/search'
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    query = {
        "q": keyword,
        "location": "us",
        "gl": "us",
        "hl": "en",
        "num": 1,
        "tbm": "shop",
        "site": "amazon"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        results = response.json().get('shopping_results')
        if results:
            return results[0]  # Tomar el primer resultado relevante
    else:
        st.error("Error al obtener datos de Amazon. Verifica tu API Key.")
        return None

# Función para estimar las ventas mensuales
def estimate_monthly_sales(price, rating, review_count):
    # Suposición de un modelo simple: ventas = (rating * review_count) / precio
    try:
        sales_estimation = (rating * review_count) / price
        # Normalizamos el resultado para un rango plausible de ventas
        estimated_sales = int(np.clip(sales_estimation * 10, 50, 10000))
        return estimated_sales
    except:
        st.error("Error en el cálculo de las ventas.")
        return None

# Configuración de la aplicación en Streamlit
st.title("Estimador de Ventas Mensuales de Libros en Amazon")

# Entrada de usuario para la palabra clave
keyword = st.text_input("Introduce una palabra clave para buscar el libro en Amazon:", "Python programming")

# Botón de búsqueda
if st.button("Estimar Ventas"):
    # Obtener datos de Amazon
    data = get_amazon_data(keyword)
    if data:
        # Extraer los datos relevantes
        book_title = data.get('title', 'Título no disponible')
        price = float(data.get('price', '0').replace('$', ''))
        rating = float(data.get('rating', '0'))
        review_count = int(data.get('reviews_count', '0').replace(',', ''))

        # Mostrar los datos obtenidos
        st.write(f"### Resultados de Amazon para '{keyword}'")
        st.write(f"**Título:** {book_title}")
        st.write(f"**Precio:** ${price}")
        st.write(f"**Rating:** {rating} / 5")
        st.write(f"**Número de Reseñas:** {review_count}")

        # Estimar ventas mensuales
        estimated_sales = estimate_monthly_sales(price, rating, review_count)
        if estimated_sales:
            st.write(f"## Estimación de Ventas Mensuales: {estimated_sales} copias")
    else:
        st.warning("No se encontraron datos relevantes para la palabra clave ingresada.")
