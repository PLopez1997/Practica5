# app.py
import streamlit as st
from modulos.venta import mostrar_venta  # Importamos la función mostrar_venta del módulo venta
from modulos.login import login

# Comprobamos si la sesión ya está iniciada
if "sesion_iniciada" in st.session_state and st.session_state["sesion_iniciada"]:
   import streamlit as st

# Mostrar el menú lateral
opciones = ["Ventas", "Otra opción"]  # Agrega más opciones si las necesitas
seleccion = st.sidebar.selectbox("Selecciona una opción", opciones)

# Según la opción seleccionada, mostramos el contenido correspondiente
if seleccion == "Ventas":
    mostrar_venta()  # Asegúrate de haber definido esta función antes
elif seleccion == "Otra opción":
    st.write("Has seleccionado otra opción.")  # Aquí podrías agregar el contenido de otras opciones

else:
    # Si la sesión no está iniciada, mostrar el login
    login()
