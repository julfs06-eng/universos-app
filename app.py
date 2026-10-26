 
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

# Estilo visual avanzado: Simula una interfaz de teléfono / Cyber-OS oscuro
st.markdown("""
    <style>
    .main {
        background-color: #050508;
        color: #f0f6fc;
    }
    .stApp {
        background: radial-gradient(circle at center, #11141d 0%, #050508 100%);
    }
    .phone-container {
        background-color: #0d1117;
        border: 2px solid #30363d;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }
    .app-icon {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        transition: 0.2s;
    }
    .app-icon:hover {
        border-color: #58a6ff;
        background-color: #1f242c;
    }
    </style>
""", unsafe_allow_html=True)

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

if "current_app" not in st.session_state:
    st.session_state.current_app = "Home"

# Barra superior estilo barra de estado de celular
col_s1, col_s2, col_s3 = st.columns([2, 4, 2])
with col_s1:
    st.caption("📶 5G  🔋 100%")
with col_s2:
    st.markdown("<p style='text-align: center; margin: 0; font-size: 14px;'><b>UNIVERSE MOBILE OS</b></p>", unsafe_allow_html=True)
with col_s3:
    current_time = datetime.now().strftime("%H:%M")
    st.caption(f"🕒 {current_time}")

st.markdown("---")

# ================= PANTALLA DE INICIO (HOME / ESCRITORIO DE APPS) =================
if st.session_state.current_app == "Home":
    st.markdown("### 📱 Pantalla Principal")
    st.caption("Selecciona una aplicación para abrirla:")

    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("🌌\nCrear Mundo", use_container_width=True):
            st.session_state.current_app = "Crear Mundo"
            st.rerun()
    with c2:
        if st.button("👤\nPersonaje", use_container_width=True):
            st.session_state.current_app = "Crear Personaje"
            st.rerun()
    with c3:
        if st.button("📊\nEstadísticas", use_container_width=True):
            st.session_state.current_app = "Estadísticas"
            st.rerun()

    c4, c5 = st.columns(2)
    with c4:
        if st.button("💬\nChat Inmersivo", use_container_width=True):
            st.session_state.current_app = "Chat Inmersivo"
            st.rerun()
    with c5:
        if st.button("⚡\nAcción / Evento", use_container_width=True):
            st.session_state.current_app = "Acción"
            st.rerun()

# ================= MÓDULO: CREAR MUNDO =================
elif st.session_state.current_app == "Crear Mundo":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
    
    st.markdown("### 🌌 Editor de Mundos")
    nombre_mundo = st.text_input("Nombre del Universo / Lore principal")
    if st.button("Guardar Mundo"):
        if nombre_mundo:
            st.session_state.data["mundos"][nombre_mundo] = {"personajes": {}, "historia": []}
            guardar_datos(st.session_state.data)
            st.success(f"¡Mundo '{nombre_mundo}' creado con éxito!")

# ================= MÓDULO: CREAR PERSONAJE =================
elif st.session_state.current_app == "Crear Personaje":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
        
    st.markdown("### 👤 Registro de Personajes")
    mundos_disponibles = list(st.session_state.data.get("mundos", {}).keys())
    
    if mundos_disponibles:
        m_sel = st.selectbox("Seleccionar Universo", mundos_disponibles)
        p_nombre = st.text_input("Nombre del Personaje")
        p_rol = st.text_input("Rol o Descripción (Ej: Estudiante, Héroe)")
        
        if st.button("Registrar Personaje"):
            if p_nombre:
                st.session_state.data["mundos"][m_sel]["personajes"][p_nombre] = {
                    "rol": p_rol,
                    "romance": 50,
                    "amistad": 50,
                    "confianza": 50,
                    "odio": 0
                }
                guardar_datos(st.session_state.data)
                st.success(f"¡Personaje '{p_nombre}' añadido al universo!")
    else:
        st.warning("Primero crea un mundo en la sección 'Crear Mundo'.")

# ================= MÓDULO: ESTADÍSTICAS =================
elif st.session_state.current_app == "Estadísticas":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
        
    st.markdown("### 📊 Panel de Relaciones y Estadísticas")
    mundos_disponibles = list(st.session_state.data.get("mundos", {}).keys())
    
    if mundos_disponibles:
        m_sel = st.selectbox("Ver Universo", mundos_disponibles, key="stat_mundo")
        personajes = st.session_state.data["mundos"][m_sel]["personajes"]
        
        if personajes:
            p_sel = st.selectbox("Seleccionar Personaje", list(personajes.keys()), key="stat_pj")
            stats = personajes[p_sel]
            
            st.markdown(f"**Estado actual con {p_sel}:**")
            st.progress(stats["romance"] / 100, text=f"Romance: {stats['romance']}%")
            st.progress(stats["amistad"] / 100, text=f"Amistad: {stats['amistad']}%")
            st.progress(stats["confianza"] / 100, text=f"Confianza: {stats['confianza']}%")
            st.progress(stats["odio"] / 100, text=f"Odio: {stats['odio']}%")
        else:
            st.info("No hay personajes en este mundo todavía.")
    else:
        st.warning("No hay mundos creados.")

# ================= MÓDULO: CHAT INMERSIVO =================
elif st.session_state.current_app == "Chat Inmersivo":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
        
    st.markdown("### 💬 Chat Inmersivo")
    st.info("Próximamente conectado con la IA para simular interacciones basadas en tus estadísticas.")

# ================= MÓDULO: ACCIÓN / EVENTO =================
elif st.session_state.current_app == "Acción":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
        
    st.markdown("### ⚡ Ejecutar Evento Dinámico")
    st.info("Aquí ocurrirán los eventos especiales que alteran el Lore y las estadísticas en tiempo real.")
        