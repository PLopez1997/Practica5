import streamlit as st
from modulos.config.conexion import obtener_conexion

def mostrar_clientes():
    st.header("👤 Gestión de Clientes")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # ---------- FORMULARIO PARA AGREGAR NUEVO CLIENTE ----------
        with st.form("form_cliente"):
            st.subheader("📝 Registrar nuevo cliente")
            nombre = st.text_input("Nombre completo")
            correo = st.text_input("Correo electrónico")
            telefono = st.text_input("Número de teléfono")
            direccion = st.text_area("Dirección")
            enviar = st.form_submit_button("✅ Guardar cliente")

            if enviar:
                if nombre.strip() == "" or correo.strip() == "":
                    st.warning("⚠ Debes ingresar al menos nombre y correo.")
                else:
                    try:
                        cursor.execute(
                            "INSERT INTO Clientes (Nombre, Correo, Telefono, Direccion) VALUES (%s, %s, %s, %s)",
                            (nombre, correo, telefono, direccion)
                        )
                        con.commit()
                        st.success(f"✅ Cliente registrado correctamente: {nombre}")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error al registrar el cliente: {e}")

        # ---------- VISUALIZAR REGISTROS EXISTENTES ----------
        st.subheader("📋 Lista de clientes registrados")

        try:
            cursor.execute(
                "SELECT ID, Nombre, Correo, Telefono, Direccion FROM Clientes ORDER BY ID DESC"
            )
            resultados = cursor.fetchall()

            if resultados:
                # Mostrar los registros en una tabla
                st.dataframe(
                    [
                        {
                            "ID": r[0],
                            "Nombre": r[1],
                            "Correo": r[2],
                            "Teléfono": r[3],
                            "Dirección": r[4]
                        } 
                        for r in resultados
                    ]
                )
            else:
                st.info("ℹ No hay clientes registrados todavía.")
        except Exception as e:
            st.error(f"❌ Error al cargar los clientes: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()

