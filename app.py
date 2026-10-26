import json
import os
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="WorldOS Mobile",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilo visual Cyber-OS / Glassmorphism
st.markdown("""
    <style>
    /* Reset y fondo general */
    .stApp {
        background: #090a0f !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Ocultar elementos nativos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Contenedor principal de la pantalla del celular */
    .mobile-frame {
        background: rgba(18, 22, 34, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 20px 15px;
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
        margin-bottom: 25px;
    }

    /* Barra de estado superior */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        color: #8b949e;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 15px;
    }

    /* Estilo para los botones tipo Iconos de Apps */
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(145deg, #161b26, #0f121a) !important;
        color: #e6edf3 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 18px !important;
        padding: 12px 6px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        border-color: #58a6ff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(88, 166, 255, 0.25) !important;
    }

    /* Burbujas de Chat */
    .chat-bubble-user {
        background: #1f6feb;
        color: white;
        padding: 10px 14px;
        border-radius: 16px 16px 2px 16px;
        margin: 6px 0 6px auto;
        max-width: 80%;
        font-size: 14px;
    }
    .chat-bubble-bot {
        background: #21262d;
        color: #e6edf3;
        border: 1px solid #30363d;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 2px;
        margin: 6px auto 6px 0;
        max-width: 80%;
        font-size: 14px;
    }

    /* Targetas para Feed / Instagram */
    .post-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 15px;
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- MARCO DEL CELULAR ---
st.markdown('<div class="mobile-frame">', unsafe_allow_html=True)

# Barra de estado
hora_actual = datetime.now().strftime("%H:%M")
st.markdown(f'''
    <div class="status-bar">
        <span>📶 5G</span>
        <span style="color: #58a6ff; font-weight: bold; font-size: 13px;">WORLD OS</span>
        <span>🕒 {hora_actual} | 🔋 100%</span>
    </div>
''', unsafe_allow_html=True)

# ================= 📱 ESCRITORIO (HOME) =================
if st.session_state.current_app == "Home":
    st.markdown("<h4 style='text-align: center; color: #f0f6fc; margin-bottom: 15px;'>📱 WorldOS Desktop</h4>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌌\nMundos"):
            st.session_state.current_app = "Crear Mundo"
            st.rerun()
        if st.button("💬\nChat IA"):
            st.session_state.current_app = "Chat Inmersivo"
            st.rerun()

    with col2:
        if st.button("👤\nPersonajes"):
            st.session_state.current_app = "Crear Personaje"
            st.rerun()
        if st.button("📸\nWorldgram"):
            st.session_state.current_app = "Redes Sociales"
            st.rerun()

    with col3:
        if st.button("📊\nStats"):
            st.session_state.current_app = "Estadísticas"
            st.rerun()
        if st.button("⚡\nEventos"):
            st.session_state.current_app = "Acción"
            st.rerun()

# ================= 🌌 CREAR MUNDO =================
elif st.session_state.current_app == "Crear Mundo":
    if st.button("⬅️ Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
    st.markdown("### 🌌 Crear Universo")
    nombre_mundo = st.text_input("Nombre del Universo (Ej: My Hero Academia)")
    if st.button("Guardar Universo"):
        if nombre_mundo:
            if nombre_mundo not in st.session_state.data["mundos"]:
                st.session_state.data["mundos"][nombre_mundo] = {"personajes": {}, "historia": []}
                guardar_datos(st.session_state.data)
                st.success(f"¡Universo '{nombre_mundo}' guardado!")
            else:
                st.warning("Ese universo ya existe.")

# ================= 👤 CREAR PERSONAJE =================
elif st.session_state.current_app == "Crear Personaje":
    if st.button("⬅️ Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
    st.markdown("### 👤 Registrar Personaje")
    mundos = list(st.session_state.data.get("mundos", {}).keys())
    if mundos:
        m_sel = st.selectbox("Universo", mundos)
        p_nom = st.text_input("Nombre (Ej: Shoto Todoroki)")
        p_rol = st.text_input("Rol / Descripción (Ej: Estudiante 1-A)")
        if st.button("Guardar Personaje"):
            if p_nom:
                st.session_state.data["mundos"][m_sel]["personajes"][p_nom] = {
                    "rol": p_rol,
                    "romance": 40,
                    "amistad": 55,
                    "confianza": 60,
                    "odio": 5
                }
                guardar_datos(st.session_state.data)
                st.success(f"¡{p_nom} registrado!")
    else:
        st.info("Primero crea un universo.")

# ================= 📊 ESTADÍSTICAS =================
elif st.session_state.current_app == "Estadísticas":
    if st.button("⬅️ Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
    st.markdown("### 📊 Panel de Vínculos")
    mundos = list(st.session_state.data.get("mundos", {}).keys())
    if mundos:
        m_sel = st.selectbox("Universo", mundos)
        pjs = st.session_state.data["mundos"][m_sel].get("personajes", {})
        if pjs:
            p_sel = st.selectbox("Personaje", list(pjs.keys()))
            st = pjs[p_sel]
            st.write(f"**Relación con {p_sel}:**")
            st.progress(st.get("romance", 50)/100, text=f"❤️ Romance: {st.get('romance', 50)}%")
            st.progress(st.get("amistad", 50)/100, text=f"🤝 Amistad: {st.get('amistad', 50)}%")
            st.progress(st.get("confianza", 50)/100, text=f"🛡️ Confianza: {st.get('confianza', 50)}%")
            st.progress(st.get("odio", 0)/100, text=f"🔥 Odio: {st.get('odio', 0)}%")
        else:
            st.info("No hay personajes creados aquí.")

# ================= 💬 CHAT INMERSIVO =================
elif st.session_state.current_app == "Chat Inmersivo":
    if st.button("⬅️ Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
    st.markdown("### 💬 Chat Directo")
    
    # Historial simulado estilo mensajería
    for msg in st.session_state.chat_history:
        if msg["sender"] == "user":
            st.markdown(f'<div class="chat-bubble-user">{msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot"><b>{msg["sender"]}:</b> {msg["text"]}</div>', unsafe_allow_html=True)

    user_text = st.text_input("Escribe tu mensaje...", key="chat_input")
    if st.button("Enviar"):
        if user_text:
            st.session_state.chat_history.append({"sender": "user", "text": user_text})
            # Respuesta automatizada simulada
            st.session_state.chat_history.append({"sender": "Shoto Todoroki", "text": "Entiendo lo que dices... Seguiré entrenando duro en la U.A."})
            st.rerun()

# ================= 📸 REDES SOCIALES (WORLDGRAM) =================
elif st.session_state.current_app == "Redes Sociales":
    if st.button("⬅️ Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
    st.markdown("### 📸 Worldgram Feed")
    
    st.markdown('''
        <div class="post-card">
            <b style="color: #58a6ff;">@shoto_official</b> <span style="font-size: 11px; color: #8b949e;">• Hace 2h</span>
            <p style="margin: 8px 0; font-size: 13px;">El entrenamiento de hoy con Midoriya y Bakugo estuvo intenso. Toca descansar un poco.</p>
            <span style="font-size: 12px; color: #f778ba;">❤️ 1,240 Me gusta</span>
        </div>
        <div class="post-card">
            <b style="color: #58a6ff;">@bakugo_dynamight</b> <span style="font-size: 11px; color: #8b949e;">• Hace 5h</span>
            <p style="margin: 8px 0; font-size: 13px;">¡¡¡NO SE METAN EN MI CAMINO SI NO QUIEREN TERMINAR EXPLOTADOS!!! 💥💥</p>
            <span style="font-size: 12px; color: #f778ba;">❤️ 3,890 Me gusta</span>
        </div>
    ''', unsafe_allow_html=True)

# ================= ⚡ EVENTOS =================
elif st.session_state.current_app == "Acción":
    if st.button("⬅️ Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
    st.markdown("### ⚡ Eventos del Lore")
    st.info("Dispara eventos aleatorios que alteran tus estadísticas.")

st.markdown('</div>', unsafe_allow_html=True)
