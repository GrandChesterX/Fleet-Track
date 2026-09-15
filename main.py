import streamlit as st
import streamlit_authenticator as stauth


#Llamo el modulo de juanjo
from vehiculos import obtener_flota_inicial
#LLamo el modulo de Carlos
from mapas_grid import renderizar_panel_y_mapa
#Llamamos el modulo aggrid y folium para trabajar con los componentes que pasa mapas_grid
from st_aggrid import AgGrid 
from streamlit_folium import st_folium

# Configuro la pagina
st.set_page_config(
    page_title="Seguimiento de Flota",
    page_icon="🚗"
)

# Añado credenciales
usuarios = {
    "usernames": {
        "admin": {
            "email": "admin@empresa.com",
            "name": "Administrador",
            "password": "admin"
        },
        "operario": {
            "email": "user@empresa.com",
            "name": "Operario JJ",
            "password": "1234"
        }
    }
}

# Inicializo el autenticador
authenticator = stauth.Authenticate(
    usuarios,
    "mi_cookie_session",
    "clave_secreta_firma",
    cookie_expiry_days=30
)

# Muestro el login
authenticator.login(
    location="main",
    fields={
        "Form name": "Iniciar Sesión",
        "Username": "Usuario",
        "Password": "Contraseña",
        "Login": "Iniciar Sesión",
    }
)

# Intentamos obtener las credenciales
authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")

# Controlamos el acceso
if authentication_status:

    st.sidebar.write(f"Bienvenido/a **{name}**")

    authenticator.logout(
        "Cerrar Sesión",
        "sidebar"
    )

    st.title("Panel de Vehículos 🚗")
    
    #Ejecutamos el modulo (obtener_flota_inicial) para cargar el df
    flota_vehiculos = obtener_flota_inicial()

    # Pasamos el df al componente de panel y mapas
    df_vehiculos, grid_options, mapa_folium = renderizar_panel_y_mapa(flota_vehiculos)

    # Renderizamos la tabla y le pasamos las variables necesarias 
    st.subheader("Panel Avanzado de Flota (AgGrid)")
    
    AgGrid(df_vehiculos, gridOptions=grid_options, fit_columns_on_grid_load=True)

    # Renderizamos el mapa y buscamos las variables que necesitamos para mostrar el mensaje
    st.subheader("Geolocalización en Vivo - Vitoria-Gasteiz")
    
    mostrar_mapa = st_folium(mapa_folium, width=700, height=500)
    
    # Comenzamos con las validaciones del mapa para poder enseñar los mensajes
    if mostrar_mapa and mostrar_mapa.get("last_object_clicked"):
        
        #Creamos dos variables para saber donde el usuario hizo click
        lat_click = mostrar_mapa["last_object_clicked"]["lat"]
        lon_click = mostrar_mapa["last_object_clicked"]["lng"]
        
        #Usamos next para buscar en base a la lat y lng los demas datos del vehiculo
        vehiculo_clic = next((v for v in flota_vehiculos if v.lat == lat_click and v.lon == lon_click), None)
    
        #Una vez encontramos el vehiculo que el usuario selecciono
        #Validamos si requiere taller usando la funcion polimorfica de vehiculos
        #Enseñamos un mensaje
        if vehiculo_clic:
            
            estado_final = "🔴 Requiere Taller" if vehiculo_clic.requiere_mantenimiento() else "🟢 Operativo"
            
            st.info(f"**Vehículo seleccionado:** {vehiculo_clic.modelo} ({vehiculo_clic.matricula}) | **Estado:** {estado_final}")

elif authentication_status is False:

    st.error("Usuario o contraseña incorrectos.")

else:

    st.info(
        "Por favor, introduce tu usuario y contraseña."
    )