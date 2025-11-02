import streamlit as st
from modulos.config.conexion import obtener_conexion

def mostrar_venta():
    st.header("🛒 Registrar venta simple")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # ---------- FORMULARIO PARA REGISTRAR VENTA ----------
        with st.form("form_venta"):
            producto = st.text_input("Nombre del producto")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            enviar = st.form_submit_button("✅ Guardar venta")

            if enviar:
                if producto.strip() == "":
                    st.warning("⚠️ Debes ingresar el nombre del producto.")
                else:
                    try:
                        cursor.execute(
                            "INSERT INTO Ventas (Producto, Cantidad) VALUES (%s, %s)",
                            (producto, cantidad)
                        )
                        con.commit()
                        st.success(f"✅ Venta registrada correctamente: {producto} (Cantidad: {cantidad})")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error al registrar la venta: {e}")

        # ---------- VISUALIZAR REGISTROS DE VENTAS ----------
        st.subheader("📋 Lista de ventas registradas")

        try:
            cursor.execute("SELECT Id_Venta, Producto, Cantidad FROM Ventas ORDER BY ID DESC")
            resultados = cursor.fetchall()

            if resultados:
                # Mostrar los registros en una tabla
                st.dataframe(
                    [
                        {
                            "Id_Venta": r[0],
                            "Producto": r[1],
                            "Cantidad": r[2]
                        }
                        for r in resultados
                    ]
                )
            else:
                st.info("ℹ No hay ventas registradas todavía.")
        except Exception as e:
            st.error(f"❌ Error al cargar las ventas: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
