import json
import os
import random
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="WorldOS - Advanced Roleplay Simulator",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados estilo interfaz móvil
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
    .story-card {
        background: #161b22;
        border-left: 4px solid #58a6ff;
        padding: 15px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 15px;
        font-size: 14px;
        line-height: 1.5;
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
                "tema": "Classic",
                "personajes": {
                    "Shoto Todoroki": {"rol": "Estudiante 1-A", "romance": 50, "amistad": 60},
                    "Katsuki Bakugo": {"rol": "Estudiante 1-A", "romance": 10, "amistad": 20},
                    "Izuku Midoriya": {"rol": "Estudiante 1-A", "romance": 30, "amistad": 80}
                },
                "apps": ["WhatsApp", "Instagram", "X (Twitter)", "Foro"],
                "historia": [
                    {"turno": 1, "texto": "Hoy tuve el examen de admisión a la U.A. La tensión en el campo de prueba era insoportable, pero logré demostrar el control de mi quirk frente a los examinadores."}
                ],
                "posts_insta": [
                    {"autor": "@akaribeaumont", "texto": "Primer día superado en la U.A. ¡Esto apenas comienza! ⚡ #FestivalDeportivoUA", "likes": 344}
                ],
                "posts_twitter": [
                    {"autor": "Ren Ui @renui", "texto": "Si la Clase 1-A sobrevive a la primera semana sin explotar los dormitorios compro boletos para todos. 🎤"}
                ]
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

if "player_profile" not in st.session_state:
    st.session_state.player_profile = {"nombre": "Akari Beaumont", "trasfondo": "Estudiante de intercambio con control elemental"}

# MARCO MÓVIL PRINCIPAL
st.markdown('<div class="phone-container">', unsafe_allow_html=True)

# BARRA DE ESTADO
hora_es = datetime.now().strftime("%H:%M")
st.markdown(f'''
    <div class="status-bar">
        <span>📶 5G  🕒 {hora_es}</span>
        <span style="color: #58a6ff; font-weight: bold;">WORLD OS MOBILE</span>
        <span>🔋 100%</span>
    </div>
''', unsafe_allow_html=True)

# BOTÓN DE RETORNO GLOBAL SI NO ESTAMOS EN HOME
if st.session_state.current_view != "Home":
    if st.button("⬅️ Volver al Menú Principal"):
        st.session_state.current_view = "Home"
        st.rerun()
    st.markdown("---")

# ================= 📱 PANTALLA PRINCIPAL / ESCRITORIO =================
if st.session_state.current_view == "Home":
    st.markdown(f"<h4 style='text-align: center; margin-bottom: 2px;'>🌌 {st.session_state.selected_world}</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #8b949e; font-size: 11px;'>Jugador: <b>{st.session_state.player_profile['nombre']}</b></p>", unsafe_allow_html=True)
    
    # Grid de Aplicaciones del SO Móvil
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📖\nRol / Story"):
            st.session_state.current_view = "StoryMode"
            st.rerun()
    with c2:
        if st.button("💬\nWhatsApp"):
            st.session_state.current_view = "WhatsApp"
            st.rerun()
    with c3:
        if st.button("📸\nInsta"):
            st.session_state.current_view = "Instagram"
            st.rerun()
    with c4:
        if st.button("🐦\nX/Tweet"):
            st.session_state.current_view = "Twitter"
            st.rerun()

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        if st.button("🤫\nForo"):
            st.session_state.current_view = "Foro"
            st.rerun()
    with c6:
        if st.button("📊\nStats"):
            st.session_state.current_view = "Stats"
            st.rerun()
    with c7:
        if st.button("🛠️\nEditor"):
            st.session_state.current_view = "EditorMundo"
            st.rerun()
    with c8:
        if st.button("➕\nCrear"):
            st.session_state.current_view = "CrearMundo"
            st.rerun()

    st.markdown("---")
    st.markdown("##### 🌐 Cambiar de Mundo Activo:")
    for m_nombre in st.session_state.data["mundos"].keys():
        if st.button(f"✨ Cargar Universo: {m_nombre}", key=f"load_{m_nombre}"):
            st.session_state.selected_world = m_nombre
            st.rerun()

# ================= 📖 MODO HISTORIA / ROL ACTIVO =================
elif st.session_state.current_view == "StoryMode":
    mundo = st.session_state.selected_world
    info_m = st.session_state.data["mundos"][mundo]
    
    st.markdown(f"### 📖 Bitácora de Historia: {mundo}")
    st.caption("La IA procesa tus acciones y actualiza dinámicamente el mundo.")

    # Mostrar historial de la historia
    for evento in info_m.get("historia", []):
        st.markdown(f'<div class="story-card"><b>Turno {evento["turno"]}:</b><br>{evento["texto"]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    nueva_accion = st.text_area("¿Qué haces o qué dicén en esta escena?", placeholder="Ej: Me acerco a Todoroki y le pregunto sobre el examen...")
    
    if st.button("▶️ Avanzar Turno y Simular IA"):
        if nueva_accion:
            nuevo_turno = len(info_m["historia"]) + 1
            # Simulación inteligente de respuesta y cambios en el mundo
            respuesta_pro = f"Tu acción ('{nueva_accion}') altera el ambiente. Shoto te mira fijamente evaluando tu fuerza, mientras Bakugo estalla de frustración a lo lejos."
            info_m["historia"].append({"turno": nuevo_turno, "texto": f"**Tú:** {nueva_accion}<br><br>💡 **IA Directora:** {respuesta_pro}"})
            
            # Modificar estadísticas de forma automática según el rol
            for p_name, p_data in info_m["personajes"].items():
                p_data["amistad"] = min(100, p_data["amistad"] + random.randint(2, 8))
                
            guardar_datos(st.session_state.data)
            st.success("¡Turno procesado y estadísticas actualizadas!")
            st.rerun()

# ================= 🛠️ CREAR Y EDITAR MUNDO =================
elif st.session_state.current_view == "CrearMundo":
    st.markdown("### ➕ Crear un Nuevo Mundo")
    nuevo_nombre = st.text_input("Nombre del Universo / Fandom", placeholder="Ej: Jujutsu Kaisen")
    nuevo_eslogan = st.text_input("Eslogan o premisa", placeholder="Ej: Maldiciones y hechicería moderna.")
    
    st.markdown("##### Configuración del Jugador")
    p_nombre = st.text_input("Tu Nombre en este mundo", value="Akari Beaumont")
    p_trasfondo = st.text_input("Tu Trasfondo / Poder", value="Hechicera de grado especial")

    if st.button("Guardar y Activar Universo"):
        if nuevo_nombre:
            st.session_state.data["mundos"][nuevo_nombre] = {
                "eslogan": nuevo_eslogan,
                "tema": "Classic",
                "personajes": {"Satoru Gojo": {"rol": "Profesor", "romance": 40, "amistad": 70}},
                "apps": ["WhatsApp", "Instagram", "X (Twitter)", "Foro"],
                "historia": [{"turno": 1, "texto": f"Inicio de la aventura para {p_nombre} en {nuevo_nombre}."}],
                "posts_insta": [],
                "posts_twitter": []
            }
            guardar_datos(st.session_state.data)
            st.session_state.selected_world = nuevo_nombre
            st.session_state.player_profile = {"nombre": p_nombre, "trasfondo": p_trasfondo}
            st.session_state.current_view = "Home"
            st.success(f"¡Universo {nuevo_nombre} creado con éxito!")
            st.rerun()

elif st.session_state.current_view == "EditorMundo":
    mundo = st.session_state.selected_world
    info_m = st.session_state.data["mundos"][mundo]
    st.markdown(f"### 🛠️ Editor: {mundo}")
    
    nuevo_eslogan = st.text_input("Editar Eslogan", value=info_m.get("eslogan", ""))
    
    st.markdown("##### 👥 Agregar Personaje al Mundo")
    c_nombre = st.text_input("Nombre del personaje (Ej: Denki Kaminari)")
    c_rol = st.text_input("Rol (Ej: Estudiante)")
    if st.button("+ Añadir Personaje"):
        if c_nombre:
            info_m["personajes"][c_nombre] = {"rol": c_rol, "romance": 20, "amistad": 50}
            guardar_datos(st.session_state.data)
            st.success(f"¡{c_nombre} añadido al mundo!")

    if st.button("💾 Guardar Cambios"):
        info_m["eslogan"] = nuevo_eslogan
        guardar_datos(st.session_state.data)
        st.success("¡Actualizado correctamente!")

# ================= 💬 WHATSAPP / CHAT GRUPAL =================
elif st.session_state.current_view == "WhatsApp":
    mundo = st.session_state.selected_world
    st.markdown(f"### 💬 WhatsApp - {mundo}")
    
    if "wa_msgs" not in st.session_state:
        st.session_state.wa_msgs = [
            {"sender": "Izuku Midoriya", "text": "¡Hola a todos! ¿Repasaron los apuntes para mañana?"},
            {"sender": "Katsuki Bakugo", "text": "¡DEJA DE MOLESTAR CON TUS APUNTES DEKU!"}
        ]

    for msg in st.session_state.wa_msgs:
        if msg["sender"] == "user":
            st.markdown(f'<div class="chat-user">{msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot"><b>{msg["sender"]}:</b> {msg["text"]}</div>', unsafe_allow_html=True)

    wa_input = st.text_input("Escribe al grupo de WhatsApp...")
    if st.button("Enviar a WhatsApp"):
        if wa_input:
            st.session_state.wa_msgs.append({"sender": "user", "text": wa_input})
            pjs = list(st.session_state.data["mundos"][mundo]["personajes"].keys())
            respondedor = random.choice(pjs) if pjs else "Bakugo"
            st.session_state.wa_msgs.append({"sender": respondedor, "text": "¡Vaya comentario tan interesante... lo tendré en cuenta!"})
            st.rerun()

# ================= 📸 INSTAGRAM =================
elif st.session_state.current_view == "Instagram":
    mundo = st.session_state.selected_world
    info_m = st.session_state.data["mundos"][mundo]
    st.markdown("### 📸 Instagram Feed")
    
    nuevo_post = st.text_input("Publicar foto/estado en Instagram...")
    if st.button("Publicar en Insta"):
        if nuevo_post:
            info_m["posts_insta"].insert(0, {"autor": f"@{st.session_state.player_profile['nombre'].lower().replace(' ', '')}", "texto": nuevo_post, "likes": 1})
            guardar_datos(st.session_state.data)
            st.success("¡Publicado en Instagram!")

    for post in info_m.get("posts_insta", []):
        st.markdown(f'''
            <div class="card-box">
                <b>{post["autor"]}</b><br>
                <p style="margin: 6px 0; font-size: 13px;">{post["texto"]}</p>
                <span style="color: #f778ba; font-size: 12px;">❤️ {post["likes"]} Me gusta</span>
            </div>
        ''', unsafe_allow_html=True)

# ================= 🐦 TWITTER / X =================
elif st.session_state.current_view == "Twitter":
    mundo = st.session_state.selected_world
    info_m = st.session_state.data["mundos"][mundo]
    st.markdown("### 🐦 X (Twitter)")
    
    tw_input = st.text_input("¿Qué está pasando? (Tweet)...")
    if st.button("Twittear"):
        if tw_input:
            info_m["posts_twitter"].insert(0, {"autor": f"{st.session_state.player_profile['nombre']} @user", "texto": tw_input})
            guardar_datos(st.session_state.data)
            st.success("¡Tweet publicado!")

    for tw in info_m.get("posts_twitter", []):
        st.markdown(f'''
            <div class="card-box">
                <b>{tw["autor"]}</b><br>
                <p style="margin: 6px 0; font-size: 13px;">{tw["texto"]}</p>
            </div>
        ''', unsafe_allow_html=True)

# ================= 🤫 FORO ANÓNIMO =================
elif st.session_state.current_view == "Foro":
    st.markdown("### 🤫 Foro Anónimo")
    st.markdown('''
        <div class="card-box">
            <b>pasillo_secreto</b><br>
            <p style="margin: 4px 0; font-size: 13px;">¿Alguien notó lo intenso que estuvo el entrenamiento hoy?</p>
        </div>
    ''', unsafe_allow_html=True)

# ================= 📊 ESTADÍSTICAS DE RELACIÓN =================
elif st.session_state.current_view == "Stats":
    mundo = st.session_state.selected_world
    pjs = st.session_state.data["mundos"][mundo].get("personajes", {})
    st.markdown(f"### 📊 Vínculos de Personajes - {mundo}")
    
    for nombre, stats in pjs.items():
        st.write(f"**{nombre}** ({stats.get('rol', '')})")
        st.progress(stats.get("romance", 50)/100, text=f"❤️ Romance: {stats.get('romance', 50)}%")
        st.progress(stats.get("amistad", 50)/100, text=f"🤝 Amistad: {stats.get('amistad', 50)}%")

st.markdown('</div>', unsafe_allow_html=True)
