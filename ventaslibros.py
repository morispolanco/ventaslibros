import streamlit as st
import requests
import json

# Título de la aplicación
st.title("Estimador de Ventas de Libros en Amazon")

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
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en la API de Serper: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión con la API de Serper: {e}")
        return None

# Función para estimar ventas basadas en los parámetros y datos de búsqueda
def estimar_ventas(titulo_o_keyword, genero, precio, promocion, formato):
    api_key = get_serper_api_key()
    if not api_key:
        return None

    # Crear una consulta basada en los parámetros del libro o keyword, enfocada en Amazon
    promocion_texto = "se está promocionando" if promocion else "no se está promocionando"
    consulta = f"ventas mensuales libros {genero} \"{titulo_o_keyword}\" formato {formato} precio {precio} dólares {promocion_texto} site:amazon.com"

    # Mostrar la consulta para depuración
    st.subheader("Consulta de Búsqueda:")
    st.code(consulta, language='plaintext')

    st.write("Realizando búsqueda para estimar ventas en Amazon...")

    resultados = realizar_busqueda(consulta, api_key)
    if not resultados:
        st.error("No se pudo obtener una respuesta válida de la API de Serper.")
        return None

    # Mostrar la respuesta completa de la API para depuración
    st.subheader("Respuesta de la API:")
    st.json(resultados)

    # Procesar los resultados de la búsqueda
    try:
        total_resultados_str = resultados.get("searchInformation", {}).get("totalResults", "0")
        total_resultados = int(total_resultados_str.replace(",", ""))
    except (ValueError, TypeError):
        total_resultados = 0

    st.write(f"Total de Resultados Encontrados: {total_resultados}")

    # Asignar factor de conversión basado en el formato y enfoque en Amazon
    if formato.lower() == "ebook":
        factor_conversion = 15  # Mayor potencial de ventas en Amazon para Ebooks
    elif formato.lower() == "softcover":
        factor_conversion = 12  # Buen equilibrio
    elif formato.lower() == "hardcover":
        factor_conversion = 10   # Menor potencial de ventas
    else:
        factor_conversion = 12  # Valor por defecto

    ventas_estimadas = total_resultados * factor_conversion

    # Ajustar ventas si se está promocionando (mercadeando)
    if promocion:
        ventas_estimadas *= 1.3  # Aumenta un 30% si se está promocionando

    return ventas_estimadas

# Interfaz de usuario para ingresar los detalles del libro
st.header("Ingrese los detalles del libro para ventas en Amazon")

# Campo para ingresar el título o keyword
titulo_o_keyword = st.text_input("Título o Keyword del Libro", "")

# Selección de género con 15 opciones
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

# Entrada de precio en dólares
precio = st.number_input("Precio ($)", min_value=0.0, step=0.5, format="%.2f")

# Selección de formato
formato = st.selectbox("Formato", [
    "Ebook",
    "Softcover",
    "Hardcover"
])

# Checkbox para indicar si se está promocionando el libro
promocion = st.checkbox("¿Se está promocionando el libro?")

# Botón para estimar ventas
if st.button("Estimar Ventas Mensuales en Amazon"):
    if not titulo_o_keyword:
        st.error("Por favor, ingrese el título o una palabra clave relacionada con el libro.")
    else:
        ventas = estimar_ventas(titulo_o_keyword, genero, precio, promocion, formato)
        if ventas is not None:
            st.success(f"Las ventas estimadas mensuales en Amazon son: {ventas:.0f} unidades.")
        else:
            st.warning("No se pudieron estimar las ventas. Revisa los detalles ingresados o intenta nuevamente.")

# Opcional: Mostrar los resultados de la búsqueda para transparencia
if st.checkbox("Mostrar resultados de búsqueda en Amazon"):
    api_key = get_serper_api_key()
    if api_key and titulo_o_keyword:
        promocion_texto = "se está promocionando" if promocion else "no se está promocionando"
        consulta = f"ventas mensuales libros {genero} \"{titulo_o_keyword}\" formato {formato} precio {precio} dólares {promocion_texto} site:amazon.com"
        resultados = realizar_busqueda(consulta, api_key)
        if resultados:
            st.subheader("Consulta de Búsqueda:")
            st.code(consulta, language='plaintext')
            st.subheader("Respuesta de la API:")
            st.json(resultados)
