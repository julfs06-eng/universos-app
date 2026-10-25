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

# Estilo visual moderno estilo interfaz de celular / cyber-sistema
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .stApp {
        background-image: linear-gradient(to bottom, #0d1117, #161b22);
    }
    .chat-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #21262d;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #30363d;
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

st.title("🌌 Universe Simulator OS")
st.caption("Versión 3 - Interfaz Inmersiva, Lore Dinámico y Rol Avanzado")

# ====================== MENÚ ======================
menu = st.sidebar.radio(
    "📱 Menú Principal",
    [
        "🏠 Inicio",
        "✨ Crear Mundo",
        "👤 Crear Personaje",
        "📊 Panel de Estadísticas",
        "💬 Chat Inmersivo",
        "⚡ Ejecutar Acción / Evento"
    ]
)

# ====================== CREAR MUNDO ======================
if menu == "✨ Crear Mundo":
    st.subheader("✨ Crear un nuevo universo")
    with st.form("form_mundo"):
        nombre_mundo = st.text_input("Nombre del mundo (ej: My Hero Academia, Harry Potter...)")
        lore = st.text_area("Historia / Lore del mundo (Contexto, reglas, ambiente, ubicaciones clave)")
        crear = st.form_submit_button("Crear Mundo en el Sistema")
        
        if crear and nombre_mundo.strip():
            if nombre_mundo in st.session_state.data["mundos"]:
                st.error("⚠️ Este mundo ya existe en la base de datos.")
            else:
                st.session_state.data["mundos"][nombre_mundo] = {
                    "lore": lore,
                    "personajes": {},
                    "bitacora": []
                }
                guardar_datos(st.session_state.data)
                st.success(f"🚀 Mundo '{nombre_mundo}' registrado con éxito.")
                st.rerun()

# ====================== CREAR PERSONAJE ======================
elif menu == "👤 Crear Personaje":
    st.subheader("👤 Configuración de Personaje")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("⚠️ Primero debes crear un mundo antes de añadir personajes.")
    else:
        mundo_seleccionado = st.selectbox("Selecciona el mundo destino", mundos)
        
        with st.form("form_personaje"):
            nombre_personaje = st.text_input("Nombre del personaje")
            descripcion = st.text_area("Descripción detallada (Personalidad, apariencia, quirk/poderes, historia)")
            
            st.markdown("### 🎚️ Parámetros Iniciales (0 - 100)")
            col1, col2 = st.columns(2)
            with col1:
                romance = st.slider("Romance", 0, 100, 10)
                amistad = st.slider("Amistad", 0, 100, 20)
            with col2:
                confianza = st.slider("Confianza", 0, 100, 15)
                odio = st.slider("Odio", 0, 100, 0)
            
            crear = st.form_submit_button("Inicializar Personaje")
            
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
                st.success(f"✨ Personaje '{nombre_personaje}' vinculado a {mundo_seleccionado}.")
                st.rerun()

# ====================== VER / EDITAR ESTADÍSTICAS ======================
elif menu == "📊 Panel de Estadísticas":
    st.subheader("📊 Panel de Control y Estadísticas")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("No hay mundos creados todavía.")
    else:
        mundo = st.selectbox("Seleccionar Mundo", mundos)
        personajes = list(st.session_state.data["mundos"][mundo]["personajes"].keys())
        
        if not personajes:
            st.info("Este mundo todavía no tiene personajes registrados.")
        else:
            personaje = st.selectbox("Seleccionar Personaje", personajes)
            datos = st.session_state.data["mundos"][mundo]["personajes"][personaje]
            
            st.markdown(f"### 🧬 Perfil: **{personaje}**")
            st.info(datos.get("descripcion", "Sin descripción"))
            
            st.markdown("#### 📈 Métricas de Relación Actuales")
            parametros = datos["parametros"]
            
            # Visualizador moderno con columnas tipo app
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💖 Romance", parametros.get("Romance", 0))
            col2.metric("🤝 Amistad", parametros.get("Amistad", 0))
            col3.metric("🛡️ Confianza", parametros.get("Confianza", 0))
            col4.metric("⚡ Odio", parametros.get("Odio", 0))
            
            with st.expander("⚙️ Ajustar parámetros manualmente"):
                nuevos = {}
                for nombre, valor in parametros.items():
                    nuevos[nombre] = st.slider(nombre, 0, 100, valor, key=f"stat_{personaje}_{nombre}")
                
                if st.button("Guardar Nuevos Valores"):
                    st.session_state.data["mundos"][mundo]["personajes"][personaje]["parametros"] = nuevos
                    guardar_datos(st.session_state.data)
                    st.success("¡Parámetros actualizados correctamente!")
                    st.rerun()

# ====================== CHAT CON PERSONAJES ======================
elif menu == "💬 Chat Inmersivo":
    st.subheader("💬 Simulación de Conversación Avanzada")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("No hay mundos creados.")
    else:
        mundo = st.selectbox("Mundo activo", mundos, key="chat_mundo")
        personajes = list(st.session_state.data["mundos"][mundo]["personajes"].keys())
        
        if not personajes:
            st.info("Este mundo no tiene personajes para iniciar el chat.")
        else:
            personaje = st.selectbox("¿Con quién deseas interactuar?", personajes, key="chat_pers")
            datos_pers = st.session_state.data["mundos"][mundo]["personajes"][personaje]
            lore_mundo = st.session_state.data["mundos"][mundo]["lore"]
            
            if "chat" not in datos_pers:
                datos_pers["chat"] = []
            
            # Panel superior de estado rápido
            p = datos_pers["parametros"]
            st.caption(f"🧠 Estado vincular con {personaje} | Romance: {p['Romance']} | Amistad: {p['Amistad']} | Confianza: {p['Confianza']} | Odio: {p['Odio']}")
            
            # Contenedor de historial de chat estilizado
            chat_container = st.container()
            with chat_container:
                for msg in datos_pers["chat"]:
                    if msg["rol"] == "usuario":
                        st.markdown(f"👤 **Tú:** {msg['texto']}")
                    else:
                        st.markdown(f"🤖 **{personaje}:** {msg['texto']}")
                    st.text(f"[{msg['hora']}]")
                    st.markdown("---")
            
            with st.form(key=f"chat_form_{personaje}", clear_on_submit=True):
                mensaje_usuario = st.text_area("Escribe tu acción o diálogo (sé tan detallada como quieras):", placeholder="Ej: *Me acerco lentamente con una sonrisa y le pregunto en qué piensa*...")
                enviar = st.form_submit_button("Enviar Mensaje")
                
                if enviar and mensaje_usuario.strip():
                    hora = datetime.now().strftime("%H:%M")
                    
                    # Guardar mensaje del usuario
                    datos_pers["chat"].append({
                        "rol": "usuario",
                        "texto": mensaje_usuario,
                        "hora": hora
                    })
                    
                    # Generador de respuesta inmersiva con memoria y contexto del lore
                    p = datos_pers["parametros"]
                    msg_lower = mensaje_usuario.lower()
                    
                    # Lógica de adaptación según parámetros y palabras clave
                    if p["Odio"] > 50 or "atacar" in msg_lower or "golpear" in msg_lower:
                        prefijos = [
                            f"Retrocede un paso con la mirada afilada, cruzando de brazos mientras la tensión en el ambiente aumenta. Frunce el ceño y responde con frialdad:",
                            f"Aprieta los dientes, notando cómo la hostilidad entre ambos es evidente. Su voz sale seca y cortante:"
                        ]
                        cuerpo = f"No me vengas con juegos. Conozco perfectamente el contexto de este lugar ({mundo}) y sé cuáles son tus intenciones. No confío en ti ni un poco."
                        p["Odio"] = min(100, p["Odio"] + 5)
                        p["Confianza"] = max(0, p["Confianza"] - 5)
                    elif p["Romance"] > 40 or "lindo" in msg_lower or "abrazo" in msg_lower or "beso" in msg_lower:
                        prefijos = [
                            f"Un rubor leve cruza por sus mejillas mientras aparta la mirada por un segundo, intentando mantener la compostura antes de murmurar:",
                            f"Su expresión se suaviza de manera notable, dejando de lado su habitual reserva para mirarte fijamente a los ojos y decir:"
                        ]
                        cuerpo = f"Es extraño... normalmente no suelo abrirme con nadie sobre lo que pasa por mi cabeza, pero contigo... supongo que es diferente. Gracias por estar aquí."
                        p["Romance"] = min(100, p["Romance"] + 6)
                        p["Amistad"] = min(100, p["Amistad"] + 4)
                    else:
                        prefijos = [
                            f"Analiza tus palabras con detenimiento, cruzando los brazos mientras evalúa la situación con calma:",
                            f"Exhala un suspiro leve, observando los alrededores antes de volverse hacia ti y comentar:"
                        ]
                        cuerpo = f"Las cosas en este entorno no son sencillas. Entre las reglas del lugar y todo lo que está pasando en {mundo}, tenemos que tener cuidado con cada movimiento que damos."
                        p["Amistad"] = min(100, p["Amistad"] + 3)

                    respuesta_ia = f"{random.choice(prefijos)} \"{cuerpo}\""
                    
                    datos_pers["chat"].append({
                        "rol": "personaje",
                        "texto": respuesta_ia,
                        "hora": hora
                    })
                    
                    guardar_datos(st.session_state.data)
                    st.rerun()

# ====================== REALIZAR ACCIÓN ======================
elif menu == "⚡ Ejecutar Acción / Evento":
    st.subheader("⚡ Sistema de Eventos y Acciones Dinámicas")
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
            accion = st.text_area("¿Qué acción compleja deseas realizar?", placeholder="Ej: Lo defendí de un peligro inminente arriesgando mi propia seguridad...")
            
            if st.button("Procesar Impacto en la Historia"):
                if accion.strip():
                    datos = st.session_state.data["mundos"][mundo]["personajes"][personaje]
                    params = datos["parametros"]
                    
                    accion_lower = accion.lower()
                    cambios_texto = []
                    
                    if any(p in accion_lower for p in ["salvar", "defender", "proteger", "ayudar", "cuidar"]):
                        params["Confianza"] = min(100, params["Confianza"] + 15)
                        params["Amistad"] = min(100, params["Amistad"] + 12)
                        params["Odio"] = max(0, params["Odio"] - 10)
                        cambios_texto.append("🛡️ Confianza y Amistad aumentaron considerablemente.")
                    elif any(p in accion_lower for p in ["atacar", "traicionar", "insultar", "golpear"]):
                        params["Odio"] = min(100, params["Odio"] + 20)
                        params["Confianza"] = max(0, params["Confianza"] - 15)
                        cambios_texto.append("⚡ ¡El Odio aumentó y la Confianza se desplomó!")
                    else:
                        params["Amistad"] = min(100, params["Amistad"] + 5)
                        cambios_texto.append("📈 Se registró un cambio neutral en la relación.")
                    
                    # Registrar en bitácora
                    if "bitacora" not in st.session_state.data["mundos"][mundo]:
                        st.session_state.data["mundos"][mundo]["bitacora"] = []
                    
                    st.session_state.data["mundos"][mundo]["bitacora"].append(
                        f"Acción con {personaje}: {accion} → {' | '.join(cambios_texto)}"
                    )
                    
                    guardar_datos(st.session_state.data)
                    
                    st.success("✨ ¡Evento procesado con éxito por el sistema!")
                    st.markdown(f"**Consecuencia narrativa:** {' | '.join(cambios_texto)}")
                    
                    st.markdown("#### 📊 Nuevos Parámetros Actualizados:")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("💖 Romance", params["Romance"])
                    col2.metric("🤝 Amistad", params["Amistad"])
                    col3.metric("🛡️ Confianza", params["Confianza"])
                    col4.metric("⚡ Odio", params["Odio"])
                else:
                    st.warning("Escribe una acción primero.")

# ====================== INICIO ======================
else:
    st.subheader("🌍 Tus Universos Activos")
    
    if not st.session_state.data["mundos"]:
        st.info("Todavía no has creado ningún mundo. Ve al menú lateral en '✨ Crear Mundo'.")
    else:
        for nombre, info in st.session_state.data["mundos"].items():
            with st.expander(f"🌌 Universo: {nombre}"):
                st.write(f"**Lore / Historia:** {info.get('lore', 'Sin historia')}")
                st.write(f"**Personajes totales:** {len(info.get('personajes', {}))}")
                
                if info.get("bitacora"):
                    st.markdown("**📜 Últimos eventos registrados:**")
                    for nota in info["bitacora"][-3:]:
                        st.caption(f"• {nota}")

st.sidebar.markdown("---")
st.sidebar.caption("Universe Simulator OS - v3.0 Inmersiva")
            
