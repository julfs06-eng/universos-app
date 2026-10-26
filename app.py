 
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

# Estilo visual avanzado: Interfaz de teléfono / Cyber-OS con efecto glassmorphism
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
        background-color: rgba(13, 17, 23, 0.85);
        border: 2px solid #30363d;
        border-radius: 28px;
        padding: 25px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    .os-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 12px;
        color: #8b949e;
        margin-bottom: 15px;
        border-bottom: 1px solid #21262d;
        padding-bottom: 8px;
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

# Contenedor estilo carcasa de celular
with st.container():
    st.markdown('<div class="phone-container">', unsafe_allow_html=True)
    
    # Barra superior de estado
    col_s1, col_s2, col_s3 = st.columns([2, 4, 2])
    with col_s1:
        st.caption("📶 5G  🔋 100%")
    with col_s2:
        st.markdown("<p style='text-align: center; margin: 0; font-size: 13px; font-weight: bold; color: #58a6ff;'>WORLD OS</p>", unsafe_allow_html=True)
    with col_s3:
        current_time = datetime.now().strftime("%H:%M")
        st.caption(f"🕒 {current_time}")

    st.markdown("---")

    # ================= PANTALLA DE INICIO (HOME / ESCRITORIO DE APPS) =================
    if st.session_state.current_app == "Home":
        st.markdown("#### 📱 Escritorio")
        st.caption("Toca una aplicación para abrirla:")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🌌\nMundos", use_container_width=True):
                st.session_state.current_app = "Crear Mundo"
                st.rerun()
        with c2:
            if st.button("👤\nPersonajes", use_container_width=True):
                st.session_state.current_app = "Crear Personaje"
                st.rerun()
        with c3:
            if st.button("📊\nEstadísticas", use_container_width=True):
                st.session_state.current_app = "Estadísticas"
                st.rerun()

        c4, c5, c6 = st.columns(3)
        with c4:
            if st.button("💬\nChat IA", use_container_width=True):
                st.session_state.current_app = "Chat Inmersivo"
                st.rerun()
        with c5:
            if st.button("📸\nRedes", use_container_width=True):
                st.session_state.current_app = "Redes Sociales"
                st.rerun()
        with c6:
            if st.button("⚡\nEventos", use_container_width=True):
                st.session_state.current_app = "Acción"
                st.rerun()

    # ================= MÓDULO: CREAR MUNDO =================
    elif st.session_state.current_app == "Crear Mundo":
        if st.button("⬅️ Volver al Escritorio"):
            st.session_state.current_app = "Home"
            st.rerun()
        
        st.markdown("### 🌌 Gestor de Universos")
        nombre_mundo = st.text_input("Nombre del Universo / Fandom (Ej: My Hero Academia)")
        if st.button("Crear Universo"):
            if nombre_mundo:
                if nombre_mundo not in st.session_state.data["mundos"]:
                    st.session_state.data["mundos"][nombre_mundo] = {"personajes": {}, "historia": []}
                    guardar_datos(st.session_state.data)
                    st.success(f"¡Universo '{nombre_mundo}' registrado!")
                else:
                    st.warning("Este universo ya existe.")

    # ================= MÓDULO: CREAR PERSONAJE =================
    elif st.session_state.current_app == "Crear Personaje":
        if st.button("⬅️ Volver al Escritorio"):
            st.session_state.current_app = "Home"
            st.rerun()
            
        st.markdown("### 👤 Registro de Personajes")
        mundos_disponibles = list(st.session_state.data.get("mundos", {}).keys())
        
        if mundos_disponibles:
            m_sel = st.selectbox("Seleccionar Universo", mundos_disponibles)
            p_nombre = st.text_input("Nombre del Personaje (Ej: Shoto Todoroki)")
            p_rol = st.text_input("Rol (Ej: Estudiante / Héroe)")
            
            if st.button("Guardar Personaje"):
                if p_nombre:
                    st.session_state.data["mundos"][m_sel]["personajes"][p_nombre] = {
                        "rol": p_rol,
                        "romance": 40,
                        "amistad": 55,
                        "confianza": 60,
                        "odio": 5
                    }
                    guardar_datos(st.session_state.data)
                    st.success(f"¡{p_nombre} añadido con éxito!")
        else:
            st.warning("Primero crea un universo en la app de Mundos.")

    # ================= MÓDULO: ESTADÍSTICAS =================
    elif st.session_state.current_app == "Estadísticas":
        if st.button("⬅️ Volver al Escritorio"):
            st.session_state.current_app = "Home"
            st.rerun()
            
        st.markdown("### 📊 Panel de Relaciones")
        mundos_disponibles = list(st.session_state.data.get("mundos", {}).keys())
        
        if mundos_disponibles:
            m_sel = st.selectbox("Ver Universo", mundos_disponibles, key="stat_mundo")
            personajes = st.session_state.data["mundos"][m_sel].get("personajes", {})
            
            if personajes:
                p_sel = st.selectbox("Seleccionar Personaje", list(personajes.keys()), key="stat_pj")
                stats = personajes[p_sel]
                
                st.markdown(f"**Vínculos con {p_sel}:**")
                st.progress(stats.get("romance", 50) / 100, text=f"Romance: {stats.get('romance', 50)}%")
                st.progress(stats.get("amistad", 50) / 100, text=f"Amistad: {stats.get('amistad', 50)}%")
                st.progress(stats.get("confianza", 50) / 100, text=f"Confianza: {stats.get('confianza', 50)}%")
                st.progress(stats.get("odio", 0) / 100, text=f"Odio: {stats.get('odio', 0)}%")
            else:
                st.info("Aún no hay personajes en este mundo.")
        else:
            st.warning("No hay universos registrados.")

    # ================= MÓDULO: CHAT INMERSIVO =================
    elif st.session_state.current_app == "Chat Inmersivo":
        if st.button("⬅️ Volver al Escritorio"):
            st.session_state.current_app = "Home"
            st.rerun()
            
        st.markdown("### 💬 Mensajes (Chat)")
        st.info("Aquí conversarán tus personajes basándose en el nivel de tus estadísticas.")

    # ================= MÓDULO: REDES SOCIALES =================
    elif st.session_state.current_app == "Redes Sociales":
        if st.button("⬅️ Volver al Escritorio"):
            st.session_state.current_app = "Home"
            st.rerun()
            
        st.markdown("### 📸 Worldgram (Feed)")
        st.info("Aquí aparecerán las publicaciones y estados de los personajes de tus fandoms.")

    # ================= MÓDULO: ACCIÓN / EVENTO =================
    elif st.session_state.current_app == "Acción":
        if st.button("⬅️ Volver al Escritorio"):
            st.session_state.current_app = "Home"
            st.rerun()
            
        st.markdown("### ⚡ Eventos del Lore")
        st.info("Dispara eventos que alterarán el destino de tus personajes.")

    st.markdown('</div>', unsafe_allow_html=True)
