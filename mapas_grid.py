import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_folium import st_folium
import folium

def renderizar_panel_y_mapa(vehiculos):
    st.subheader("Panel Avanzado de Flota (AgGrid)")
# se crea los datos delos vehiculos 
    data = [{
        "Matrícula": v.matricula,
        "Modelo": v.modelo,
        "Kilómetros": v.kilometros,
        "Estado Taller": "Requiere Taller" if v.requiere_mantenimiento() else "Operativo",
        "Latitud": v.lat,
        "Longitud": v.lon
    } for v in vehiculos]

    df = pd.DataFrame(data)
 # se crea las tablas utilizando Agrid
    gb = GridOptionsBuilder.from_dataframe(df)
    
    gb.configure_selection(selection_mode='single', use_checkbox=True)
    grid_options = gb.build()
    
    AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True)

    st.subheader("Geolocalización en Vivo - Vitoria-Gasteiz")
    m = folium.Map(location=[42.8467, -2.6716], zoom_start=13)

    for v in vehiculos:
        color = 'red' if v.requiere_mantenimiento() else 'green'
        estado_texto = "Requiere Taller" if v.requiere_mantenimiento() else "Operativo"
        
        folium.Marker(
            [v.lat, v.lon],
            popup=f"<b>{v.modelo}</b><br>Matrícula: {v.matricula}<br>Estado: {estado_texto}",
            icon=folium.Icon(color=color, icon='truck', prefix='fa')
        ).add_to(m)

    mostrar_mapa = st_folium(m, width=700, height=500)
    
    if mostrar_mapa and mostrar_mapa.get("last_clicked"):
        lat_click = mostrar_mapa["last_clicked"]["lat"]
        lon_click = mostrar_mapa["last_clicked"]["lng"]
        st.info(f"Coordenadas seleccionadas en el mapa: Lat {lat_click}, Lon {lon_click}")