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
def estimar_ventas(titulo, genero, precio, promocion):
    api_key = get_serper_api_key()
    if not api_key:
        return None

    # Crear una consulta basada en los parámetros del libro
    promocion_texto = "se está promocionando" if promocion else "no se está promocionando"
    consulta = f"ventas mensuales libros {genero} '{titulo}' precio {precio} euros {promocion_texto}"

    st.write("Realizando búsqueda para estimar ventas...")

    resultados = realizar_busqueda(consulta, api_key)
    if not resultados:
        return None

    # Aquí puedes personalizar cómo procesar los resultados de la búsqueda
    # Para este ejemplo, simplemente contamos el número de resultados y los usamos como base
    # para la estimación. En una aplicación real, querrías analizar los datos más detalladamente.

    try:
        total_resultados = resultados.get("searchInformation", {}).get("totalResults", "0")
        total_resultados = int(total_resultados)
    except (ValueError, TypeError):
        total_resultados = 0

    # Lógica simple de estimación: supongamos que cada resultado representa potenciales ventas
    # Multiplicamos por un factor para simular la conversión
    factor_conversion = 10  # Este factor puede ajustarse basado en datos reales
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
precio = st.number_input("Precio (€)", min_value=0.0, step=0.5)
promocion = st.checkbox("¿Se está promocionando el libro?")

# Botón para estimar ventas
if st.button("Estimar Ventas Mensuales"):
    if not titulo:
        st.error("Por favor, ingrese el título del libro.")
    else:
        ventas = estimar_ventas(titulo, genero, precio, promocion)
        if ventas is not None:
            st.success(f"Las ventas estimadas mensuales son: {ventas} unidades.")

# Opcional: Mostrar los resultados de la búsqueda para transparencia
if st.checkbox("Mostrar resultados de búsqueda"):
    api_key = get_serper_api_key()
    if api_key and titulo:
        promocion_texto = "se está promocionando" if promocion else "no se está promocionando"
        consulta = f"ventas mensuales libros {genero} '{titulo}' precio {precio} euros {promocion_texto}"
        resultados = realizar_busqueda(consulta, api_key)
        if resultados:
            st.json(resultados)
