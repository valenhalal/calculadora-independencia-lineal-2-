import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Calculadora Álgebra", page_icon="🧮")
st.title("🧮 Super Calculadora de Álgebra Lineal")

# --- MENÚ PRINCIPAL ---
opcion = st.selectbox(
    "MENÚ PRINCIPAL: Elige una opción",
    ["1. Determinar Independencia Lineal", "2. Verificar si un vector pertenece al Espacio Generado (Span)"]
)

st.divider()

# --- INGRESO DE VECTORES ---
st.subheader("Ingreso de Vectores")
if opcion.startswith("1"):
    st.write("Escribe los **vectores del conjunto**. (Uno por línea, números separados por espacio)")
else:
    st.write("Escribe los **vectores GENERADORES** (la base de tu espacio). (Uno por línea, números separados por espacio)")

# Caja de texto grande para los vectores
texto_vectores = st.text_area("Introduce tus vectores aquí:", height=150, placeholder="Ejemplo:\n1 2 3\n4 5 6")

# Si elige la opción 2, mostramos la caja para el vector objetivo
if opcion.startswith("2"):
    texto_objetivo = st.text_input("Vector objetivo a verificar:", placeholder="Ejemplo: 5 8 11")

# --- BOTÓN DE CÁLCULO ---
if st.button("🚀 Calcular", type="primary"):
    
    if not texto_vectores.strip():
        st.warning("⚠️ No introdujiste ningún vector. Por favor, escribe al menos uno.")
    else:
        try:
            lista_de_vectores = []
            lineas = texto_vectores.strip().split('\n')
            dimension = 0
            error_dimension = False

            # Procesamos cada línea escrita
            for linea in lineas:
                if linea.strip(): # Ignoramos líneas vacías
                    vector_convertido = [sp.Rational(x) for x in linea.split()]
                    
                    # Seguro contra accidentes: verificar la dimensión
                    if len(lista_de_vectores) == 0:
                        dimension = len(vector_convertido)
                    elif len(vector_convertido) != dimension:
                        st.error(f"❌ Error: Un vector tiene {len(vector_convertido)} componentes, pero los anteriores tienen {dimension}. Asegúrate de que todos sean del mismo tamaño.")
                        error_dimension = True
                        break # Rompemos el ciclo si hay error
                        
                    lista_de_vectores.append(vector_convertido)

            # Si todos los vectores están bien, procedemos a calcular
            if not error_dimension:
                matriz = sp.Matrix(lista_de_vectores).T

                st.divider()
                st.subheader("Resultados:")

                # --- LÓGICA OPCIÓN 1: Independencia Lineal ---
                if opcion.startswith("1"):
                    espacio_nulo = matriz.nullspace()
                    
                    if len(espacio_nulo) == 0:
                        st.success("✅ **Resultado: Son Linealmente INDEPENDIENTES.**")
                    else:
                        st.warning("⚠️ **Resultado: Son Linealmente DEPENDIENTES.**")
                        for indice, solucion in enumerate(espacio_nulo):
                            st.write(f"**--- Relación de dependencia #{indice + 1} ---**")
                            constantes = solucion.tolist()
                            ecuacion = []
                            for i, c in enumerate(constantes):
                                valor = c[0]
                                st.write(f"C{i+1}: `{valor}`")
                                if valor != 0:
                                    ecuacion.append(f"({valor})*v{i+1}")
                            st.code(" + ".join(ecuacion) + " = 0", language="math")

                # --- LÓGICA OPCIÓN 2: Espacio Generado (Span) ---
                elif opcion.startswith("2"):
                    if not texto_objetivo.strip():
                        st.error("❌ Error: Debes ingresar el vector objetivo para verificar el Span.")
                    else:
                        vector_objetivo = [sp.Rational(x) for x in texto_objetivo.split()]
                        
                        if len(vector_objetivo) != dimension:
                            st.error(f"❌ Error: El vector objetivo debe tener exactamente {dimension} componentes para coincidir con los generadores.")
                        else:
                            # Matemáticas para el Span
                            v_obj = sp.Matrix(vector_objetivo)
                            matriz_ampliada = matriz.row_join(v_obj)

                            if matriz.rank() == matriz_ampliada.rank():
                                st.success("✅ **Resultado: EL VECTOR SÍ PERTENECE AL ESPACIO GENERADO.**")
                                st.write("Se puede construir mezclando los vectores generadores.")
                                
                                solucion, parametros_libres = matriz.gauss_jordan_solve(v_obj)
                                constantes = solucion.col(0).tolist()
                                
                                st.write("Las constantes para construirlo son:")
                                ecuacion = []
                                for i in range(len(constantes)):
                                    valor = constantes[i][0]
                                    st.write(f"Constante C{i+1}: `{valor}`")
                                    if valor != 0:
                                        ecuacion.append(f"({valor})*v{i+1}")
                                        
                                st.write("Ecuación demostrativa:")
                                st.code(" + ".join(ecuacion) + " = Vector Objetivo", language="math")
                            else:
                                st.error("⚠️ **Resultado: EL VECTOR NO PERTENECE AL ESPACIO GENERADO.**")
                                st.write("No existe ninguna combinación de los generadores que dé como resultado este vector.")

        except ValueError:
            st.error("❌ Error: Asegúrate de escribir solo números separados por espacios.")
        except Exception as e:
            st.error(f"❌ Ocurrió un error matemático: {e}")
