def estimar_ventas(titulo_o_keyword, genero, precio, promocion, formato):
    api_key = get_serper_api_key()
    if not api_key:
        return None

    # Crear una consulta simplificada
    consulta = f"libros {genero} '{titulo_o_keyword}' site:amazon.com"

    # Mostrar la consulta para depuración
    st.subheader("Consulta de Búsqueda:")
    st.code(consulta, language='plaintext')

    st.write("Realizando búsqueda para estimar ventas en Amazon...")

    resultados = realizar_busqueda(consulta, api_key)
    if not resultados:
        return None

    # Mostrar la respuesta completa de la API para depuración
    st.subheader("Respuesta de la API:")
    st.json(resultados)

    # Procesar los resultados de la búsqueda
    try:
        total_resultados = int(resultados.get("searchInformation", {}).get("totalResults", "0"))
    except (ValueError, TypeError):
        total_resultados = 0

    st.write(f"Total de Resultados Encontrados: {total_resultados}")

    # Usar un factor de conversión fijo para la estimación
    factor_conversion = 10

    ventas_estimadas = total_resultados * factor_conversion

    # Ajustar ventas si se está promocionando (mercadeando)
    if promocion:
        ventas_estimadas *= 1.3  # Aumenta un 30% si se está promocionando

    return ventas_estimadas
