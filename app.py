import json
import os
import streamlit as st

st.set_page_config(
    page_title="Universe Simulator OS",
    page_icon="🌌",
    layout="centered"
)

DB_FILE = "estado_universos.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"mundos": {}}

def guardar_datos(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Cargar datos
if "data" not in st.session_state:
    st.session_state.data = cargar_datos()

st.title("🌌 Universe Simulator OS")
st.caption("Versión 1 - Mundos, Personajes y Parámetros")

# ====================== MENÚ ======================
menu = st.sidebar.radio(
    "Menú",
    ["🏠 Inicio", "✨ Crear Mundo", "👤 Crear Personaje", "📊 Ver / Editar Estadísticas"]
)

# ====================== CREAR MUNDO ======================
if menu == "✨ Crear Mundo":
    st.subheader("Crear un nuevo universo")
    
    with st.form("form_mundo"):
        nombre_mundo = st.text_input("Nombre del mundo (ej: MHA, Harry Potter...)")
        lore = st.text_area("Historia / Lore del mundo")
        crear = st.form_submit_button("Crear Mundo")
        
        if crear and nombre_mundo.strip():
            if nombre_mundo in st.session_state.data["mundos"]:
                st.error("Ese mundo ya existe.")
            else:
                st.session_state.data["mundos"][nombre_mundo] = {
                    "lore": lore,
                    "personajes": {}
                }
                guardar_datos(st.session_state.data)
                st.success(f"Mundo '{nombre_mundo}' creado correctamente.")
                st.rerun()

# ====================== CREAR PERSONAJE ======================
elif menu == "👤 Crear Personaje":
    st.subheader("Crear personaje")
    
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("Primero debes crear un mundo.")
    else:
        mundo_seleccionado = st.selectbox("Selecciona el mundo", mundos)
        
        with st.form("form_personaje"):
            nombre_personaje = st.text_input("Nombre del personaje")
            descripcion = st.text_area("Descripción del personaje")
            
            st.markdown("### Parámetros iniciales")
            romance = st.slider("Romance", 0, 100, 10)
            amistad = st.slider("Amistad", 0, 100, 20)
            confianza = st.slider("Confianza", 0, 100, 15)
            odio = st.slider("Odio", 0, 100, 0)
            
            crear = st.form_submit_button("Crear Personaje")
            
            if crear and nombre_personaje.strip():
                st.session_state.data["mundos"][mundo_seleccionado]["personajes"][nombre_personaje] = {
                    "descripcion": descripcion,
                    "parametros": {
                        "Romance": romance,
                        "Amistad": amistad,
                        "Confianza": confianza,
                        "Odio": odio
                    }
                }
                guardar_datos(st.session_state.data)
                st.success(f"Personaje '{nombre_personaje}' creado en {mundo_seleccionado}.")
                st.rerun()

# ====================== VER / EDITAR ESTADÍSTICAS ======================
elif menu == "📊 Ver / Editar Estadísticas":
    st.subheader("Estadísticas de personajes")
    
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("No hay mundos creados todavía.")
    else:
        mundo = st.selectbox("Mundo", mundos)
        personajes = list(st.session_state.data["mundos"][mundo]["personajes"].keys())
        
        if not personajes:
            st.info("Este mundo todavía no tiene personajes.")
        else:
            personaje = st.selectbox("Personaje", personajes)
            datos_personaje = st.session_state.data["mundos"][mundo]["personajes"][personaje]
            
            st.markdown(f"### {personaje}")
            st.write(datos_personaje.get("descripcion", "Sin descripción"))
            
            st.markdown("#### Parámetros actuales")
            
            parametros = datos_personaje["parametros"]
            nuevos_valores = {}
            
            for nombre_param, valor in parametros.items():
                nuevos_valores[nombre_param] = st.slider(
                    nombre_param, 0, 100, valor, key=f"{personaje}_{nombre_param}"
                )
            
            if st.button("Guardar cambios"):
                st.session_state.data["mundos"][mundo]["personajes"][personaje]["parametros"] = nuevos_valores
                guardar_datos(st.session_state.data)
                st.success("Parámetros actualizados.")
                st.rerun()

# ====================== INICIO ======================
else:
    st.subheader("Mundos creados")
    
    if not st.session_state.data["mundos"]:
        st.info("Todavía no has creado ningún mundo. Ve a la sección 'Crear Mundo'.")
    else:
        for nombre, info in st.session_state.data["mundos"].items():
            with st.expander(f"🌍 {nombre}"):
                st.write(f"**Lore:** {info.get('lore', 'Sin historia')}")
                st.write(f"**Personajes:** {len(info.get('personajes', {}))}")

st.sidebar.markdown("---")
st.sidebar.caption("Versión 1 lista. Después agregamos las apps y las acciones.")
