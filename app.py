import json
import os
import random
import streamlit as st
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="WorldOS - Mobile Simulator",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados para replicar la experiencia de interfaz estilo celular
st.markdown("""
    <style>
    /* Estructura general */
    .stApp {
        background-color: #0d1117 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    #MainMenu, footer, header { visibility: hidden; }

    /* Marco del Smartphone */
    .phone-screen {
        background: #161b22;
        border: 2px solid #30363d;
        border-radius: 32px;
        padding: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        margin-bottom: 20px;
    }

    /* Isla dinámica / Barra superior */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        color: #8b949e;
        padding: 4px 8px 12px 8px;
    }
    .dynamic-island {
        width: 80px;
        height: 18px;
        background: #000;
        border-radius: 10px;
    }

    /* Cuadrícula de Apps estilo iPhone/Android */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 8px !important;
    }
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: unset !important;
    }

    /* Botones estilo icono de App */
    div.stButton > button {
        width: 100% !important;
        background: #21262d !important;
        color: #f0f6fc !important;
        border: 1px solid #30363d !important;
        border-radius: 18px !important;
        padding: 12px 2px !important;
        font-size: 11px !important;
        font-weight: 500 !important;
    }
    div.stButton > button:hover {
        border-color: #58a6ff !important;
        background: #30363d !important;
    }

    /* Mensajes de WhatsApp */
    .chat-msg-user {
        background: #005c4b;
        color: #e9edef;
        padding: 8px 12px;
        border-radius: 12px 12px 0px 12px;
        margin: 4px 0 4px auto;
        max-width: 80%;
        font-size: 13px;
    }
    .chat-msg-bot {
        background: #202c33;
        color: #e9edef;
        padding: 8px 12px;
        border-radius: 12px 12px 12px 0px;
        margin: 4px auto 4px 0;
        max-width: 80%;
        font-size: 13px;
    }

    /* Tarjetas de Posts / Twitter / Instagram */
    .post-box {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
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

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"sender": "Izuku Midoriya", "text": "¡Hola a todos! ¿Alguien tiene los apuntes del entrenamiento de hoy?"},
        {"sender": "Katsuki Bakugo", "text": "¡¡¡A NADIE LE IMPORTAN TUS APUNTES DEKU BASTARDO!!!"},
        {"sender": "Shoto Todoroki", "text": "Los tengo yo. Te los paso por privado."}
    ]

# MARCO MÓVIL
st.markdown('<div class="phone-screen">', unsafe_allow_html=True)

# BARRA SUPERIOR
hora_actual = datetime.now().strftime("%H:%M")
st.markdown(f'''
    <div class="status-bar">
        <span>{hora_actual}</span>
        <div class="dynamic-island"></div>
        <span>📶 5G 🔋 100%</span>
    </div>
''', unsafe_allow_html=True)

# NAV INFERIOR O BOTÓN DE INICIO
if st.session_state.current_app != "Home":
    if st.button("⬅️ Pantalla de Inicio (Home)"):
        st.session_state.current_app = "Home"
        st.rerun()
    st.markdown("---")

# ================= 📱 ESCRITORIO DE APPS (HOME) =================
if st.session_state.current_app == "Home":
    st.markdown("<h5 style='text-align: center; color: #8b949e;'>WorldOS - Pantalla Principal</h5>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💬\nWhatsApp"):
            st.session_state.current_app = "WhatsApp"
            st.rerun()
    with col2:
        if st.button("📸\nInstagram"):
            st.session_state.current_app = "Instagram"
            st.rerun()
    with col3:
        if st.button("🐦\nX (Twitter)"):
            st.session_state.current_app = "Twitter"
            st.rerun()
    with col4:
        if st.button("🤫\nForo"):
            st.session_state.current_app = "Foro"
            st.rerun()

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        if st.button("📊\nStats"):
            st.session_state.current_app = "Stats"
            st.rerun()
    with col6:
        if st.button("🏆\nLogros"):
            st.session_state.current_app = "Logros"
            st.rerun()
    with col7:
        if st.button("🌌\nMundos"):
            st.session_state.current_app = "Mundos"
            st.rerun()
    with col8:
        if st.button("⚙️\nAjustes"):
            st.session_state.current_app = "Ajustes"
            st.rerun()

# ================= 💬 WHATSAPP =================
elif st.session_state.current_app == "WhatsApp":
    st.markdown("### 💬 WhatsApp - Clase 1-A")
    
    for msg in st.session_state.chat_messages:
        if msg["sender"] == "user":
            st.markdown(f'<div class="chat-msg-user">{msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-msg-bot"><b>{msg["sender"]}:</b> {msg["text"]}</div>', unsafe_allow_html=True)

    user_text = st.text_input("Escribe un mensaje al grupo...", key="input_wa")
    if st.button("Enviar"):
        if user_text:
            st.session_state.chat_messages.append({"sender": "user", "text": user_text})
            # Simulación de respuesta en grupo
            respuestas = [
                {"sender": "Katsuki Bakugo", "text": "¡¡¡CÁLLATE Y NO DIGAS TONTERÍAS!!!"},
                {"sender": "Shoto Todoroki", "text": "Coincido con la idea. Hay que mantener la calma."},
                {"sender": "Mina Ashido", "text": "¡Jajaja esto se está poniendo divertido! 💖"}
            ]
            st.session_state.chat_messages.append(random.choice(respuestas))
            st.rerun()

# ================= 📸 INSTAGRAM =================
elif st.session_state.current_app == "Instagram":
    st.markdown("### 📸 Instagram Feed")
    st.markdown('''
        <div class="post-box">
            <b>@akaribeaumont</b> • Hace 2h<br>
            <p style="margin: 8px 0;">Medalla de bronce y el cielo de Musutafu de fondo. Gracias por el apoyo a todos 🥇✨ #FestivalDeportivoUA</p>
            <span style="color: #f778ba; font-size: 12px;">❤️ 344 Me gusta</span>
        </div>
    ''', unsafe_allow_html=True)

# ================= 🐦 TWITTER / X =================
elif st.session_state.current_app == "Twitter":
    st.markdown("### 🐦 X (Twitter)")
    st.markdown('''
        <div class="post-box">
            <b>Ren Ui</b> <span style="color:#8b949e;">@renui</span><br>
            <p style="margin: 6px 0;">Si la Clase 1-A hace karaoke después del festival yo pago el boleto. ¡Esto es un caos anunciado! 😭🎤 #FestivalDeportivoUA</p>
        </div>
    ''', unsafe_allow_html=True)

# ================= 🤫 FORO ANÓNIMO =================
elif st.session_state.current_app == "Foro":
    st.markdown("### 🤫 Foro Anónimo U.A.")
    st.markdown('''
        <div class="post-box">
            <b>tribuna_norte</b><br>
            <p style="margin: 4px 0;">¿Alguien más notó que Todoroki no usó el fuego en toda la final?</p>
        </div>
    ''', unsafe_allow_html=True)

# ================= 📊 ESTADÍSTICAS =================
elif st.session_state.current_app == "Stats":
    st.markdown("### 📊 Vínculos & Estadísticas")
    st.progress(1.0, text="Afecto con Hawks: 100%")
    st.progress(1.0, text="Confianza con Hawks: 100%")
    st.progress(0.1, text="Tensión Romántica: 10%")

# ================= 🏆 LOGROS =================
elif st.session_state.current_app == "Logros":
    st.markdown("### 🏆 Logros Desbloqueados")
    st.success("🥇 ¡Héroe número uno! - Desbloqueado")
    st.success("🤝 ¡Nuevos amigos! - Desbloqueado")

# ================= 🌌 MUNDOS =================
elif st.session_state.current_app == "Mundos":
    st.markdown("### 🌌 Gestor de Mundos")
    st.info("Mundo Activo: My Hero Academia")

# ================= ⚙️ AJUSTES =================
elif st.session_state.current_app == "Ajustes":
    st.markdown("### ⚙️ Ajustes del Sistema")
    st.text_input("Nombre de usuario", value="Fresita---666")

st.markdown('</div>', unsafe_allow_html=True)
