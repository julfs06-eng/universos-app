import json
import os
import random
import streamlit as st
from datetime import datetime

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

if "data" not in st.session_state:
    st.session_state.data = cargar_datos()

st.title("🌌 Universe Simulator OS")
st.caption("Versión 2 - Mundos + Chat + Acciones")

# ====================== MENÚ ======================
menu = st.sidebar.radio(
    "Menú",
    [
        "🏠 Inicio",
        "✨ Crear Mundo",
        "👤 Crear Personaje",
        "📊 Ver / Editar Estadísticas",
        "💬 Chat con Personajes",
        "⚡ Realizar Acción"
    ]
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
                    "personajes": {},
                    "bitacora": []
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
                    },
                    "chat": []
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
            datos = st.session_state.data["mundos"][mundo]["personajes"][personaje]
            
            st.markdown(f"### {personaje}")
            st.write(datos.get("descripcion", "Sin descripción"))
            
            st.markdown("#### Parámetros actuales")
            parametros = datos["parametros"]
            nuevos = {}
            
            for nombre, valor in parametros.items():
                nuevos[nombre] = st.slider(nombre, 0, 100, valor, key=f"{personaje}_{nombre}")
            
            if st.button("Guardar cambios"):
                st.session_state.data["mundos"][mundo]["personajes"][personaje]["parametros"] = nuevos
                guardar_datos(st.session_state.data)
                st.success("Parámetros actualizados.")
                st.rerun()

# ====================== CHAT CON PERSONAJES ======================
elif menu == "💬 Chat con Personajes":
    st.subheader("Chat individual")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("No hay mundos creados.")
    else:
        mundo = st.selectbox("Mundo", mundos, key="chat_mundo")
        personajes = list(st.session_state.data["mundos"][mundo]["personajes"].keys())
        
        if not personajes:
            st.info("Este mundo no tiene personajes.")
        else:
            personaje = st.selectbox("¿Con quién quieres hablar?", personajes, key="chat_pers")
            datos = st.session_state.data["mundos"][mundo]["personajes"][personaje]
            
            if "chat" not in datos:
                datos["chat"] = []
            
            st.markdown(f"### Conversación con **{personaje}**")
            
            for msg in datos["chat"]:
                if msg["rol"] == "usuario":
                    st.markdown(f"**Tú:** {msg['texto']}")
                else:
                    st.markdown(f"**{personaje}:** {msg['texto']}")
                st.caption(msg["hora"])
            
            with st.form(key=f"chat_{personaje}", clear_on_submit=True):
                mensaje = st.text_area("Escribe tu mensaje o rol:")
                enviar = st.form_submit_button("Enviar")
                
                if enviar and mensaje.strip():
                    hora = datetime.now().strftime("%H:%M")
                    
                    # Mensaje del usuario
                    datos["chat"].append({
                        "rol": "usuario",
                        "texto": mensaje,
                        "hora": hora
                    })
                    
                    # Respuesta simple del personaje
                    respuestas = [
                        "Interesante... cuéntame más.",
                        "Hmm, no estoy seguro de eso.",
                        "Eso podría complicar las cosas.",
                        "Entiendo. Seguiré observando.",
                        "Hay más en juego de lo que crees...",
                        "¿Y qué esperas que haga yo?"
                    ]
                    respuesta = random.choice(respuestas)
                    
                    datos["chat"].append({
                        "rol": "personaje",
                        "texto": respuesta,
                        "hora": hora
                    })
                    
                    guardar_datos(st.session_state.data)
                    st.rerun()

# ====================== REALIZAR ACCIÓN ======================
elif menu == "⚡ Realizar Acción":
    st.subheader("Realizar una acción")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("No hay mundos creados.")
    else:
        mundo = st.selectbox("Mundo", mundos, key="accion_mundo")
        personajes = list(st.session_state.data["mundos"][mundo]["personajes"].keys())
        
        if not personajes:
            st.info("Este mundo no tiene personajes.")
        else:
            personaje = st.selectbox("Personaje involucrado", personajes, key="accion_pers")
            accion = st.text_area("¿Qué hiciste?", placeholder="Ej: Salí a comer helado con él/ella")
            
            if st.button("Ejecutar Acción"):
                if accion.strip():
                    datos = st.session_state.data["mundos"][mundo]["personajes"][personaje]
                    params = datos["parametros"]
                    
                    # Lógica simple de consecuencias
                    accion_lower = accion.lower()
                    cambios = []
                    
                    if any(p in accion_lower for p in ["helado", "cita", "beso", "abrazo", "románt", "salí con", "invitar"]):
                        params["Romance"] = min(100, params["Romance"] + random.randint(8, 18))
                        params["Amistad"] = min(100, params["Amistad"] + random.randint(3, 8))
                        cambios.append("Romance y Amistad subieron")
                    
                    elif any(p in accion_lower for p in ["ayud", "proteger", "salvar", "regalo", "apoyar"]):
                        params["Amistad"] = min(100, params["Amistad"] + random.randint(10, 20))
                        params["Confianza"] = min(100, params["Confianza"] + random.randint(5, 12))
                        cambios.append("Amistad y Confianza subieron")
                    
                    elif any(p in accion_lower for p in ["insult", "gritar", "golpear", "traicion", "mentir", "odio"]):
                        params["Odio"] = min(100, params["Odio"] + random.randint(10, 25))
                        params["Confianza"] = max(0, params["Confianza"] - random.randint(8, 15))
                        params["Romance"] = max(0, params["Romance"] - random.randint(5, 12))
                        cambios.append("Odio subió, Confianza y Romance bajaron")
                    
                    else:
                        params["Amistad"] = min(100, params["Amistad"] + random.randint(2, 6))
                        cambios.append("Amistad subió un poco")
                    
                    # Guardar en bitácora del mundo
                    if "bitacora" not in st.session_state.data["mundos"][mundo]:
                        st.session_state.data["mundos"][mundo]["bitacora"] = []
                    
                    st.session_state.data["mundos"][mundo]["bitacora"].append(
                        f"Acción con {personaje}: {accion} → {', '.join(cambios)}"
                    )
                    
                    guardar_datos(st.session_state.data)
                    
                    st.success("¡Acción procesada!")
                    st.write(f"**Consecuencia:** {', '.join(cambios)}")
                    st.write("Parámetros actuales:")
                    st.json(params)
                else:
                    st.warning("Escribe una acción primero.")

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
                
                if info.get("bitacora"):
                    st.markdown("**Últimas acciones:**")
                    for nota in info["bitacora"][-3:]:
                        st.caption(f"• {nota}")

st.sidebar.markdown("---")
st.sidebar.caption("Versión 2 lista")
