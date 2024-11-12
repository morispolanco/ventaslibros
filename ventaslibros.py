import streamlit as st
import requests

def get_amazon_data(keyword):
    """Obtiene datos de Amazon usando la API de Serper."""
    api_key = st.secrets["SERPER_API_KEY"] # Accede a la clave desde los secretos
    if not api_key:
        st.error("API Key de Serper no encontrada en los secretos.")
        return None

    url = "https://api.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    params = {
        "q": keyword,
        "engine": "amazon",
        "location": "us"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener datos de Amazon: {e}")
        return None

def estimate_sales(amazon_data):
    """Estima las ventas mensuales utilizando un modelo simple."""
    try:
        ranking = amazon_data['data'][0]['rank']
        estimated_sales = 10000 / (ranking + 1)
        return estimated_sales
    except (KeyError, IndexError):
        st.warning("No se pudo extraer el ranking de Amazon. Asegúrate de que la palabra clave sea válida y que la API devuelva datos.")
        return None


st.title("Estimador de Ventas de Libros de Amazon")

keyword = st.text_input("Introduce la palabra clave del libro (ej: 'El Hobbit'):")

if st.button("Estimar Ventas"):
    amazon_data = get_amazon_data(keyword)
    if amazon_data:
        estimated_sales = estimate_sales(amazon_data)
        if estimated_sales:
            st.success(f"Estimación de ventas mensuales: {estimated_sales:.2f} unidades")
