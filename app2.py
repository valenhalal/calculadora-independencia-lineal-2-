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
instruccion = "vectores del conjunto" if opcion.startswith("1") else "vectores GENERADORES"
st.write(f"Escribe los **{instruccion}**. (Uno por línea, números separados por espacio)")

texto_vectores = st.text_area("Introduce tus vectores aquí:", height=150, placeholder="Ejemplo:\n1 0\n0 1\n1 1")

if opcion.startswith("2"):
    texto_objetivo = st.text_input("Vector objetivo a verificar:", placeholder="Ejemplo: 5 8")

# --- BOTÓN DE CÁLCULO ---
if st.button("🚀 Calcular", type="primary"):
    
    if not texto_vectores.strip():
        st.warning("⚠️ No introdujiste ningún vector.")
    else:
        try:
            lista_de_vectores = []
            lineas = texto_vectores.strip().split('\n')
            dimension = 0
            error_dimension = False

            for linea in lineas:
                if linea.strip():
                    vector_convertido = [sp.Rational(x) for x in linea.split()]
                    if len(lista_de_vectores) == 0:
                        dimension = len(vector_convertido)
                    elif len(vector_convertido) != dimension:
                        st.error(f"❌ Error: Dimensiones incompatibles ({len(vector_convertido)} vs {dimension}).")
                        error_dimension = True
                        break
                    lista_de_vectores.append(vector_convertido)

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
                        st.write("Se han encontrado las siguientes relaciones de dependencia:")
                        
                        for idx, solucion in enumerate(espacio_nulo):
                            st.markdown(f"**Relación #{idx + 1}:**")
                            constantes = [c[0] for c in solucion.tolist()]
                            
                            # 1. Mostrar la ecuación igualada a cero
                            ecuacion_cero = []
                            for i, c in enumerate(constantes):
                                if c != 0:
                                    ecuacion_cero.append(f"({c})v_{i+1}")
                            st.latex(" + ".join(ecuacion_cero) + " = \\vec{0}")

                            # 2. MOSTRAR DEPENDENCIA EXPLÍCITA (Despejando un vector)
                            # Buscamos el último vector que tenga constante distinta de cero para despejarlo
                            indice_despejar = -1
                            for i in range(len(constantes)-1, -1, -1):
                                if constantes[i] != 0:
                                    indice_despejar = i
                                    break
                            
                            if indice_despejar != -1:
                                c_despejar = constantes[indice_despejar]
                                terminos_derecha = []
                                for i, c in enumerate(constantes):
                                    if i != indice_despejar and c != 0:
                                        # Al pasar al otro lado del igual, el signo cambia (-c / c_despejar)
                                        coeficiente = -c / c_despejar
                                        terminos_derecha.append(f"({coeficiente})v_{i+1}")
                                
                                st.write("Esto significa que:")
                                st.latex(f"v_{indice_despejar + 1} = " + " + ".join(terminos_derecha))

                # --- LÓGICA OPCIÓN 2: Espacio Generado (Span) ---
                elif opcion.startswith("2"):
                    if not texto_objetivo.strip():
                        st.error("❌ Falta el vector objetivo.")
                    else:
                        vector_objetivo = [sp.Rational(x) for x in texto_objetivo.split()]
                        if len(vector_objetivo) != dimension:
                            st.error(f"❌ El objetivo debe tener {dimension} componentes.")
                        else:
                            v_obj = sp.Matrix(vector_objetivo)
                            matriz_ampliada = matriz.row_join(v_obj)

                            if matriz.rank() == matriz_ampliada.rank():
                                st.success("✅ **Resultado: EL VECTOR SÍ PERTENECE AL ESPACIO.**")
                                solucion, _ = matriz.gauss_jordan_solve(v_obj)
                                constantes = [c[0] for c in solucion.col(0).tolist()]
                                
                                ecuacion = []
                                for i, c in enumerate(constantes):
                                    if c != 0:
                                        ecuacion.append(f"({c})v_{i+1}")
                                st.latex("\\text{Vector Objetivo} = " + " + ".join(ecuacion))
                            else:
                                st.error("⚠️ **Resultado: EL VECTOR NO PERTENECE AL ESPACIO.**")

        except Exception as e:
            st.error(f"❌ Error en los datos: {e}")
