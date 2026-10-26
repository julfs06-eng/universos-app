import json
import os
import random
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="WorldOS Advanced Simulator",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS de alta fidelidad estilo Cyber-OS móvil
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #f0f6fc;
    }
    #MainMenu, footer, header { visibility: hidden; }

    .phone-container {
        background: #111622;
        border: 2px solid #30363d;
        border-radius: 30px;
        padding: 18px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.85);
        margin-bottom: 25px;
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        color: #8b949e;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 15px;
    }
    .card-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 12px;
    }
    div.stButton > button {
        background: #21262d !important;
        color: #f0f6fc !important;
        border: 1px solid #30363d !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        border-color: #58a6ff !important;
        background: #30363d !important;
    }
    .chat-user {
        background: #1f6feb;
        color: white;
        padding: 10px 14px;
        border-radius: 16px 16px 2px 16px;
        margin: 6px 0 6px auto;
        max-width: 80%;
        font-size: 13px;
    }
    .chat-bot {
        background: #21262d;
        color: #e6edf3;
        border: 1px solid #30363d;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 2px;
        margin: 6px auto 6px 0;
        max-width: 80%;
        font-size: 13px;
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
    return {
        "mundos": {
            "My Hero Academia": {
                "eslogan": "Academia U.A. / Sociedad de Héroes bajo tensión extrema.",
                "cover": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600",
                "personajes": {
                    "Shoto Todoroki": {"rol": "Estudiante 1-A", "romance": 60, "amistad": 80},
                    "Katsuki Bakugo": {"rol": "Estudiante 1-A", "romance": 20, "amistad": 40}
                },
                "apps": ["WhatsApp", "Instagram", "X (Twitter)", "Foro"]
            }
        }
    }

def guardar_datos(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "data" not in st.session_state:
    st.session_state.data = cargar_datos()

if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"

if "selected_world" not in st.session_state:
    st.session_state.selected_world = "My Hero Academia"

if "world_tab" not in st.session_state:
    st.session_state.world_tab = "Básicos"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"sender": "Izuku Midoriya", "text": "¡Hola! ¿Listos para el entrenamiento de quirks?"},
        {"sender": "Katsuki Bakugo", "text": "¡APARTÉNSE O LOS VOY A EXPLOTAR A TODOS!"}
    ]

# MARCO DE LA INTERFAZ MÓVIL
st.markdown('<div class="phone-container">', unsafe_allow_html=True)

# BARRA DE ESTADO
hora_es = datetime.now().strftime("%H:%M")
st.markdown(f'''
    <div class="status-bar">
        <span>📶 5G  🕒 {hora_es}</span>
        <span style="color: #58a6ff; font-weight: bold;">WORLD OS</span>
        <span>🔋 100%</span>
    </div>
''', unsafe_allow_html=True)

# BOTÓN DE RETORNO GLOBAL SI NO ESTAMOS EN HOME
if st.session_state.current_view != "Home":
    if st.button("⬅️ Volver al Escritorio / Menú"):
        st.session_state.current_view = "Home"
        st.rerun()
    st.markdown("---")

# ================= 📱 PANTALLA PRINCIPAL (HOME / ESCRITORIO) =================
if st.session_state.current_view == "Home":
    st.markdown("<h4 style='text-align: center; margin-bottom: 5px;'>📱 WorldOS Desktop</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #8b949e; font-size: 12px;'>Mundo activo: <b>{st.session_state.selected_world}</b></p>", unsafe_allow_html=True)
    
    # Cuadrícula de Apps estilo Teléfono
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("💬\nChat"):
            st.session_state.current_view = "WhatsApp"
            st.rerun()
    with c2:
        if st.button("📸\nInsta"):
            st.session_state.current_view = "Instagram"
            st.rerun()
    with c3:
        if st.button("🐦\nX/Tweet"):
            st.session_state.current_view = "Twitter"
            st.rerun()
    with c4:
        if st.button("🤫\nForo"):
            st.session_state.current_view = "Foro"
            st.rerun()

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        if st.button("📊\nStats"):
            st.session_state.current_view = "Stats"
            st.rerun()
    with c6:
        if st.button("🏆\nLogros"):
            st.session_state.current_view = "Logros"
            st.rerun()
    with c7:
        if st.button("⚙️\nEditor"):
            st.session_state.current_view = "EditorMundo"
            st.rerun()
    with c8:
        if st.button("🌌\nMundos"):
            st.session_state.current_view = "SelectorMundos"
            st.rerun()

# ================= ⚙️ EDITOR DE MUNDO (CON PESTAÑAS) =================
elif st.session_state.current_view == "EditorMundo":
    mundo_actual = st.session_state.selected_world
    st.markdown(f"### 🛠️ Configurar: {mundo_actual}")
    
    # Pestañas superiores del editor
    t1, t2, t3 = st.columns(3)
    with t1:
        if st.button("📋 Básicos", use_container_width=True):
            st.session_state.world_tab = "Básicos"
    with t2:
        if st.button("👤 Personajes", use_container_width=True):
            st.session_state.world_tab = "Personajes"
    with t3:
        if st.button("🧩 Apps", use_container_width=True):
            st.session_state.world_tab = "Apps"
            
    st.markdown("---")
    
    info = st.session_state.data["mundos"][mundo_actual]
    
    if st.session_state.world_tab == "Básicos":
        nuevo_eslogan = st.text_input("Eslogan del mundo", value=info.get("eslogan", ""))
        nueva_cover = st.text_input("URL de imagen de portada", value=info.get("cover", ""))
        
        if nueva_cover:
            st.image(nueva_cover, use_column_width=True)
            
        if st.button("💾 Guardar Cambios Básicos"):
            info["eslogan"] = nuevo_eslogan
            info["cover"] = nueva_cover
            guardar_datos(st.session_state.data)
            st.success("¡Cambios guardados con éxito!")
            
    elif st.session_state.world_tab == "Personajes":
        st.markdown("##### Agregar Personaje")
        p_nombre = st.text_input("Nombre del personaje")
        p_rol = st.text_input("Rol o descripción")
        if st.button("+ Registrar Personaje"):
            if p_nombre:
                info["personajes"][p_nombre] = {"rol": p_rol, "romance": 50, "amistad": 50}
                guardar_datos(st.session_state.data)
                st.success(f"¡{p_nombre} agregado correctamente!")
                
        st.markdown("##### Personajes actuales:")
        for p, d in info.get("personajes", {}).items():
            st.markdown(f"- **{p}**: {d.get('rol', '')}")
            
    elif st.session_state.world_tab == "Apps":
        st.markdown("##### Apps Instaladas en este mundo")
        for app in info.get("apps", []):
            st.markdown(f"✅ **{app}** (Activa)")

# ================= 💬 WHATSAPP / CHAT INTERACTIVO =================
elif st.session_state.current_view == "WhatsApp":
    st.markdown("### 💬 WhatsApp - Grupo Clase 1-A")
    
    for msg in st.session_state.chat_history:
        if msg["sender"] == "user":
            st.markdown(f'<div class="chat-user">{msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot"><b>{msg["sender"]}:</b> {msg["text"]}</div>', unsafe_allow_html=True)

    user_msg = st.text_input("Escribe tu mensaje...", key="input_chat")
    if st.button("Enviar Mensaje"):
        if user_msg:
            st.session_state.chat_history.append({"sender": "user", "text": user_msg})
            # Respuesta automatizada de los personajes del mundo
            personajes_disponibles = list(st.session_state.data["mundos"][st.session_state.selected_world]["personajes"].keys())
            personaje_que_responde = random.choice(personajes_disponibles) if personajes_disponibles else "Katsuki Bakugo"
            
            respuestas_ia = [
                f"¡No digas tonterías sobre eso!",
                f"Entiendo perfectamente lo que dices, lo tendré en cuenta.",
                f"¡¡¡DEJAME EN PAZ CON ESAS ESTUPIDECES Deku/Extra!!!",
                f"Muy interesante punto de vista..."
            ]
            st.session_state.chat_history.append({"sender": personaje_que_responde, "text": random.choice(respuestas_ia)})
            st.rerun()

# ================= 📸 INSTAGRAM =================
elif st.session_state.current_view == "Instagram":
    st.markdown("### 📸 Instagram Feed")
    st.markdown('''
        <div class="card-box">
            <b>@akaribeaumont</b> • U.A. High<br>
            <p style="margin: 8px 0; font-size: 13px;">Entrenamiento completado en la Zona Simulada. ¡Cada vez más fuertes! ⚡🔥 #FestivalDeportivoUA</p>
            <span style="color: #f778ba; font-size: 12px;">❤️ 412 Me gusta</span>
        </div>
    ''', unsafe_allow_html=True)

# ================= 🐦 TWITTER / X =================
elif st.session_state.current_view == "Twitter":
    st.markdown("### 🐦 X (Twitter)")
    st.markdown('''
        <div class="card-box">
            <b>Ren Ui</b> <span style="color:#8b949e;">@renui</span><br>
            <p style="margin: 6px 0; font-size: 13px;">Si la 1-A hace desastre en los dormitorios otra vez, juro que me mudo. #FestivalDeportivoUA</p>
        </div>
    ''', unsafe_allow_html=True)

# ================= 🤫 FORO ANÓNIMO =================
elif st.session_state.current_view == "Foro":
    st.markdown("### 🤫 Foro Anónimo")
    st.markdown('''
        <div class="card-box">
            <b>pasillo_1a</b><br>
            <p style="margin: 4px 0; font-size: 13px;">¿Alguien sabe por qué Bakugo estaba gritándole al casillero esta mañana?</p>
        </div>
    ''', unsafe_allow_html=True)

# ================= 📊 ESTADÍSTICAS =================
elif st.session_state.current_view == "Stats":
    st.markdown("### 📊 Vínculos con Personajes")
    mundo_sel = st.session_state.selected_world
    pjs = st.session_state.data["mundos"][mundo_sel].get("personajes", {})
    for nombre, stats in pjs.items():
        st.write(f"**{nombre}** ({stats.get('rol', '')})")
        st.progress(stats.get("romance", 50)/100, text=f"❤️ Romance: {stats.get('romance', 50)}%")
        st.progress(stats.get("amistad", 50)/100, text=f"🤝 Amistad: {stats.get('amistad', 50)}%")

# ================= 🏆 LOGROS =================
elif st.session_state.current_view == "Logros":
    st.markdown("### 🏆 Logros")
    st.success("🥇 ¡Héroe número uno! - Desbloqueado")
    st.success("🤝 ¡Nuevos amigos! - Desbloqueado")

# ================= 🌌 SELECTOR DE MUNDOS =================
elif st.session_state.current_view == "SelectorMundos":
    st.markdown("### 🌌 Mis Mundos")
    nuevo_mundo = st.text_input("Crear nuevo mundo / Fandom")
    if st.button("Crear Universo"):
        if nuevo_mundo and nuevo_mundo not in st.session_state.data["mundos"]:
            st.session_state.data["mundos"][nuevo_mundo] = {
                "eslogan": "Nuevo universo creado desde cero.",
                "cover": "",
                "personajes": {},
                "apps": ["WhatsApp", "Instagram"]
            }
            guardar_datos(st.session_state.data)
            st.success(f"¡Mundo '{nuevo_mundo}' creado!")
            
    st.markdown("---")
    st.markdown("##### Seleccionar activo:")
    for m in st.session_state.data["mundos"].keys():
        if st.button(f"✨ Activar: {m}", key=f"sel_{m}"):
            st.session_state.selected_world = m
            st.session_state.current_view = "Home"
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
