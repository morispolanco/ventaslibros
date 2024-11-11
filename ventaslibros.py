import streamlit as st
import requests
import json

# Título de la aplicación
st.title("Estimador de Ventas de Libros")

# Función para obtener la API Key de Serper desde los secrets
def get_serper_api_key():
    try:
        return st.secrets["serper"]["api_key"]
    except KeyError:
        st.error("La API Key de Serper no está configurada en los secrets de Streamlit.")
        return None

# Función para realizar una búsqueda usando la API de Serper
def realizar_busqueda(query, api_key):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error en la API de Serper: {response.status_code}")
        return None

# Función para estimar ventas basadas en los parámetros y datos de búsqueda
def estimar_ventas(titulo, genero, precio, promocion, formato):
    api_key = get_serper_api_key()
    if not api_key:
        return None

    # Crear una consulta basada en los parámetros del libro
    promocion_texto = "se está promocionando" if promocion else "no se está promocionando"
    consulta = f"ventas mensuales libros {genero} '{titulo}' formato {formato} precio {precio} dólares {promocion_texto}"

    st.write("Realizando búsqueda para estimar ventas...")

    resultados = realizar_busqueda(consulta, api_key)
    if not resultados:
        return None

    # Procesar los resultados de la búsqueda
    try:
        total_resultados = resultados.get("searchInformation", {}).get("totalResults", "0")
        total_resultados = int(total_resultados)
    except (ValueError, TypeError):
        total_resultados = 0

    # Asignar factor de conversión basado en el formato
    if formato.lower() == "ebook":
        factor_conversion = 12  # Mayor potencial de ventas
    elif formato.lower() == "softcover":
        factor_conversion = 10  # Buen equilibrio
    elif formato.lower() == "hardcover":
        factor_conversion = 8   # Menor potencial de ventas
    else:
        factor_conversion = 10  # Valor por defecto

    ventas_estimadas = total_resultados * factor_conversion

    # Ajustar ventas si se está promocionando (mercadeando)
    if promocion:
        ventas_estimadas *= 1.3  # Aumenta un 30% si se está promocionando

    return ventas_estimadas

# Interfaz de usuario para ingresar los detalles del libro
st.header("Ingrese los detalles del libro")

titulo = st.text_input("Título del Libro", "")
genero = st.selectbox("Género", [
    "Ficción", 
    "No Ficción", 
    "Ciencia", 
    "Historia", 
    "Biografía", 
    "Fantasía", 
    "Misterio", 
    "Romance", 
    "Thriller", 
    "Terror", 
    "Poesía", 
    "Autoayuda", 
    "Infantil", 
    "Juvenil", 
    "Desarrollo Personal",
    "Otro"
])

precio = st.number_input("Precio ($)", min_value=0.0, step=0.5)

formato = st.selectbox("Formato", [
    "Ebook",
    "Softcover",
    "Hardcover"
])

promocion = st.checkbox("¿Se está promocionando el libro?")

# Botón para estimar ventas
if st.button("Estimar Ventas Mensuales"):
    if not titulo:
        st.error("Por favor, ingrese el título del libro.")
    else:
        ventas = estimar_ventas(titulo, genero, precio, promocion, formato)
        if ventas is not None:
            st.success(f"Las ventas estimadas mensuales son: {ventas} unidades.")

# Opcional: Mostrar los resultados de la búsqueda para transparencia
if st.checkbox("Mostrar resultados de búsqueda"):
    api_key = get_serper_api_key()
    if api_key and titulo:
        promocion_texto = "se está promocionando" if promocion else "no se está promocionando"
        consulta = f"ventas mensuales libros {genero} '{titulo}' formato {formato} precio {precio} dólares {promocion_texto}"
        resultados = realizar_busqueda(consulta, api_key)
        if resultados:
            st.json(resultados)
