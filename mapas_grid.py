import pandas as pd # Importamos pandas para trabajar con datos y tablas
from st_aggrid import GridOptionsBuilder # Importamos la herramienta para configurar la tabla AgGrid
import folium # Importamos folium para crear el mapa interactivo

# Función que recibe la lista de objetos vehículo y prepara todo para la interfaz
def renderizar_panel_y_mapa(vehiculos):
    # 1. Creamos una lista de diccionarios recorriendo los objetos de la flota
    data = [{
        "Matrícula": v.matricula, # Mostramos la matrícula del vehiculo
        "Modelo": v.modelo, # Mostramos el modelo del vehiculo
        "Kilómetros": v.get_kilometros(), # Usamos el getter para obtener los kilómetros del vehiculo
        # Usamos un if  para indicar el estado del vehiculo
        "Estado Taller": "Requiere Taller" if v.requiere_mantenimiento() else "Operativo",
        "Latitud": v.lat, # Extraemos latitud
        "Longitud": v.lon # Extraemos longitud
    } for v in vehiculos] # Este bucle for llena la lista 'data'

    #  Convertimos los datos de los vehículos en un DataFrame
    df = pd.DataFrame(data)
    
    # 2. Configuramos la tabla avanzada AgGrid usando nuestro DataFrame
    gb = GridOptionsBuilder.from_dataframe(df)
    # Añadimos la opción de seleccionar una sola fila con una casilla (checkbox)
    gb.configure_selection(selection_mode='single', use_checkbox=True)
    # Construimos las opciones finales de la tabla
    grid_options = gb.build()

    # 3. Creamos el mapa base de Folium centrado en Vitoria-Gasteiz
    m = folium.Map(location=[42.8467, -2.6716], zoom_start=13)

    # 4. Usamos iterrows() para recorrer las filas del DataFrame
    for index, row in df.iterrows():
        # Si la columna 'Estado Taller' dice 'Requiere Taller', el color será rojo, si no, verde
        color = 'red' if row["Estado Taller"] == "Requiere Taller" else 'green'
        
        # Añadimos un marcador al mapa en las coordenadas exactas de esta fila
        folium.Marker(
            location=[row["Latitud"], row["Longitud"]], # Coordenadas del marcador
            # Creamos el texto del globo (popup) mezclando HTML y datos del DataFrame
            popup=f"<b>{row['Modelo']}</b><br>Matrícula: {row['Matrícula']}<br>Estado: {row['Estado Taller']}",
            # Configuramos el icono del marcador, su color y el tipo (truck = camión)
            icon=folium.Icon(color=color, icon='truck', prefix='fa')
        ).add_to(m) # Añadimos el marcador al mapa 'm'

    # La función devuelve tres cosas: el DataFrame, las opciones de la tabla y el mapa terminado
    return df, grid_options, m