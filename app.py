import json
import os
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="WorldOS Advanced",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos avanzados para replicar la interfaz de tarjetas, temas y menús flotantes
st.markdown("""
    <style>
    .stApp {
        background: #0b0e14 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #f0f6fc;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Contenedor principal estilo móvil */
    .mobile-frame {
        background: #111622;
        border: 1px solid #21262d;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.8);
        margin-bottom: 30px;
    }

    /* Tarjetas de opciones / mundos */
    .card-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        transition: 0.2s;
    }
    .card-box:hover {
        border-color: #58a6ff;
    }

    /* Botones de acción general */
    div.stButton > button {
        background: #21262d !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #30363d !important;
        border-color: #58a6ff !important;
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

if "current_view" not in st.session_state:
    st.session_state.current_view = "explorar"

if "selected_mundo" not in st.session_state:
    st.session_state.selected_mundo = None

if "mundo_tab" not in st.session_state:
    st.session_state.mundo_tab = "Básicos"

# ================= VISTA PRINCIPAL: EXPLORAR / MUNDOS =================
if st.session_state.current_view == "explorar":
    st.markdown("### 🌌 Mis Mundos")
    
    # Barra superior de navegación rápida
    col_top1, col_top2 = st.columns(2)
    with col_top1:
        if st.button("✨ Creados", use_container_width=True):
            pass
    with col_top2:
        if st.button("➕ Crear un mundo", use_container_width=True):
            st.session_state.current_view = "crear_mundo_paso1"
            st.rerun()

    st.markdown("---")

    mundos = st.session_state.data.get("mundos", {})
    if mundos:
        for nombre_m, info in mundos.items():
            st.markdown(f"""
                <div class="card-box">
                    <h4 style="margin:0; color:#58a6ff;">🌌 {nombre_m}</h4>
                    <p style="font-size:12px; color:#8b949e; margin:5px 0;">Universo activo con {len(info.get('personajes', {}))} personajes.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Abrir {nombre_m}", key=f"btn_{nombre_m}"):
                st.session_state.selected_mundo = nombre_m
                st.session_state.current_view = "gestor_mundo"
                st.rerun()
    else:
        st.info("No tienes mundos creados. ¡Empieza creando uno nuevo con el botón de arriba!")

# ================= CREAR UN MUNDO (PASO A PASO) =================
elif st.session_state.current_view == "crear_mundo_paso1":
    if st.button("⬅️ Volver"):
        st.session_state.current_view = "explorar"
        st.rerun()

    st.markdown("### 🛠️ Crear un mundo")
    st.caption("Configuración inicial del universo y su estética.")

    nombre_partida = st.text_input("Nombre de la partida / Universo", placeholder="Ej: My Hero Academia")
    eslogan = st.text_input("Eslogan o descripción corta")
    
    st.markdown("##### 🎨 Tema (Skin visual)")
    tema_seleccionado = st.selectbox(
        "Skin para la interfaz", 
        ["Classic (Azul)", "Cyberpunk (Neón)", "Kraft (Madera/Tierra)", "Sakura (Rosa)", "War Room (Militar)"]
    )

    if st.button("Guardar y Continuar", use_container_width=True):
        if nombre_partida:
            if nombre_partida not in st.session_state.data["mundos"]:
                st.session_state.data["mundos"][nombre_partida] = {
                    "eslogan": eslogan,
                    "tema": tema_seleccionado,
                    "personajes": {},
                    "apps_instaladas": ["Chat", "Estadísticas", "Historia"]
                }
                guardar_datos(st.session_state.data)
                st.session_state.selected_mundo = nombre_partida
                st.session_state.current_view = "gestor_mundo"
                st.rerun()
            else:
                st.warning("Este mundo ya existe.")

# ================= GESTOR DEL MUNDO SELECCIONADO =================
elif st.session_state.current_view == "gestor_mundo":
    mundo_actual = st.session_state.selected_mundo
    
    if st.button("⬅️ Volver a mis mundos"):
        st.session_state.current_view = "explorar"
        st.rerun()

    st.markdown(f"## ⚙️ Configurando: {mundo_actual}")

    # Pestañas superiores estilo la app de referencia
    t1, t2, t3 = st.columns(3)
    with t1:
        if st.button("📋 Básicos", use_container_width=True):
            st.session_state.mundo_tab = "Básicos"
    with t2:
        if st.button("👤 Personajes", use_container_width=True):
            st.session_state.mundo_tab = "Personajes"
    with t3:
        if st.button("🧩 Apps", use_container_width=True):
            st.session_state.mundo_tab = "Apps"

    st.markdown("---")

    # CONTENIDO SEGÚN LA PESTAÑA SELECCIONADA
    if st.session_state.mundo_tab == "Básicos":
        st.markdown("#### 📝 Ajustes Básicos")
        info_mundo = st.session_state.data["mundos"][mundo_actual]
        nuevo_eslogan = st.text_input("Eslogan", value=info_mundo.get("eslogan", ""))
        if st.button("Actualizar Cambios"):
            info_mundo["eslogan"] = nuevo_eslogan
            guardar_datos(st.session_state.data)
            st.success("¡Actualizado con éxito!")

    elif st.session_state.mundo_tab == "Personajes":
        st.markdown("#### 👥 Personajes del Universo")
        info_mundo = st.session_state.data["mundos"][mundo_actual]
        
        p_nombre = st.text_input("Nombre del personaje")
        p_rol = st.text_input("Rol / Descripción")
        if st.button("+ Agregar personaje"):
            if p_nombre:
                info_mundo["personajes"][p_nombre] = {"rol": p_rol, "romance": 50, "amistad": 50}
                guardar_datos(st.session_state.data)
                st.success(f"¡Personaje {p_nombre} añadido!")

        st.markdown("--- *Personajes actuales:*")
        for p, details in info_mundo.get("personajes", {}).items():
            st.markdown(f"- **{p}**: {details.get('rol', 'Sin rol')}")

    elif st.session_state.mundo_tab == "Apps":
        st.markdown("#### 🧩 Apps Instaladas en este Mundo")
        info_mundo = st.session_state.data["mundos"][mundo_actual]
        
        apps_actuales = info_mundo.get("apps_instaladas", [])
        for app in apps_actuales:
            st.markdown(f"""
                <div class="card-box" style="display:flex; justify-content:space-between; align-items:center;">
                    <span>📱 <b>{app}</b> (Activa)</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.info("Pronto podrás instalar más apps personalizadas como Worldgram, mapas o registros de misiones.")

# Barra inferior flotante fija de navegación general
st.markdown("---")
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    if st.button("🌐 Explorar", use_container_width=True):
        st.session_state.current_view = "explorar"
        st.rerun()
with col_b2:
    if st.button("💬 Historial", use_container_width=True):
        pass
with col_b3:
    if st.button("👤 Perfil", use_container_width=True):
        pass
