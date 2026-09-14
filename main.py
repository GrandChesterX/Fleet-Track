import streamlit as st
import streamlit_authenticator as stauth
#Llamo el modulo de juanjo
from vehiculos import obtener_flota_inicial
#LLamo el modulo de Carlos
from mapas_grid import renderizar_panel_y_mapa

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

# Moestro el login
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

    st.title("Panel de Vehiculos 🚗")

    st.success(
        f"Has accedido exitosamente como **{username}**."
    )

    
    # Tengo que llamar a los datos de a subido juanjo
    flota_vehiculos = obtener_flota_inicial()

    # LLamo al componente de Carlos que renderiza la tabla y el mapa
    renderizar_panel_y_mapa(flota_vehiculos)

elif authentication_status is False:

    st.error("Usuario o contraseña incorrectos.")

else:

    st.info(
        "Por favor, introduce tu usuario y contraseña."
    )