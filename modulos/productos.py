import streamlit as st
from modulos.config.conexion import obtener_conexion
import pandas as pd

def mostrar_productos():
    st.header("📦 Gestión de Productos")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # 🧾 Formulario para registrar nuevos productos
        with st.form("form_productos"):
            nombre = st.text_input("Nombre del producto")
            precio = st.number_input("Precio ($)", min_value=0.01, step=0.01, format="%.2f")
            stock = st.number_input("Stock disponible", min_value=0, step=1)
            enviar = st.form_submit_button("✅ Guardar producto")

            if enviar:
                if nombre.strip() == "":
                    st.warning("⚠️ Debes ingresar el nombre del producto.")
                else:
                    try:
                        cursor.execute(
                            "INSERT INTO Productos (Nombre, Precio, Stock) VALUES (%s, %s, %s)",
                            (nombre, precio, stock)
                        )
                        con.commit()
                        st.success(f"✅ Producto registrado: {nombre} (Precio: ${precio:.2f}, Stock: {stock})")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error al registrar el producto: {e}")

        # 📋 Mostrar productos registrados
        st.subheader("📄 Lista de productos registrados")

        try:
            cursor.execute("SELECT ID, Nombre, Precio, Stock FROM Productos")
            productos = cursor.fetchall()

            if productos:
                df = pd.DataFrame(productos, columns=["ID", "Nombre", "Precio ($)", "Stock"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("📭 No hay productos registrados aún.")
        except Exception as e:
            st.error(f"❌ Error al cargar los productos: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
