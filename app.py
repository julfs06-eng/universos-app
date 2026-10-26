
        import json
import os
import random
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="WorldOS - Universe Simulator",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ====================== ESTILO VISUAL WORLDOS (GLASSMORPHISM & DARK UI) ======================
st.markdown("""
    <style>
    /* Estilos globales */
    .stApp {
        background-color: #0b0e14;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header principal WorldOS */
    .worldos-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #312e81;
        padding: 18px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .worldos-header h2 {
        color: #818cf8;
        margin: 0;
        font-size: 22px;
        font-weight: 700;
    }
    .worldos-header p {
        color: #94a3b8;
        margin: 4px 0 0 0;
        font-size: 12px;
    }

    /* Tarjetas de Contenido / Apps */
    .app-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
        backdrop-filter: blur(10px);
    }
    
    /* Tags de categorías */
    .tag-pill {
        background: #312e81;
        color: #c7d2fe;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
        margin-right: 5px;
    }
    
    /* Ocultar barra lateral por defecto para enfocar en experiencia app */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
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

if "tab_activa" not in st.session_state:
    st.session_state.tab_activa = "Explorar"

# ====================== HEADER Y MENÚ SUPERIOR ======================
st.markdown("""
    <div class="worldos-header">
        <h2>✨ WorldOS Engine</h2>
        <p>Simulador de Universos & Rol Multimódulo</p>
    </div>
""", unsafe_allow_html=True)

# Navegación estilo pestañas móviles
col_t1, col_t2, col_t3, col_t4 = st.columns(4)
with col_t1:
    if st.button("🧩 Explorar", use_container_width=True):
        st.session_state.tab_activa = "Explorar"
        st.rerun()
with col_t2:
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.tab_activa = "Chat"
        st.rerun()
with col_t3:
    if st.button("⚡ Apps", use_container_width=True):
        st.session_state.tab_activa = "Apps"
        st.rerun()
with col_t4:
    if st.button("⚙️ Crear", use_container_width=True):
        st.session_state.tab_activa = "Crear"
        st.rerun()

st.markdown("---")

# ====================== PESTAÑA 1: EXPLORAR MUNDOS ======================
if st.session_state.tab_activa == "Explorar":
    st.markdown("### 🌍 Tus Universos Activos")
    
    if not st.session_state.data["mundos"]:
        st.info("Aún no tienes mundos creados. Ve a la pestaña '⚙️ Crear' para empezar tu primer universo.")
    else:
        for nombre_m, info_m in st.session_state.data["mundos"].items():
            st.markdown(f"""
                <div class="app-card">
                    <span class="tag-pill">Universo</span>
                    <span class="tag-pill">U.A. High</span>
                    <h3 style="margin: 8px 0 4px 0; color: #f8fafc;">{nombre_m}</h3>
                    <p style="color: #94a3b8; font-size: 13px;">{info_m.get('lore', 'Sin lore definido')[:120]}...</p>
                    <p style="color: #818cf8; font-size: 12px;">👥 Personajes: {len(info_m.get('personajes', {}))} | 📱 Apps activas: {len(info_m.get('apps', ['Chat', 'Acciones']))}</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"🔍 Ver detalles de {nombre_m}"):
                st.write("**Lore completo:**", info_m.get("lore", ""))
                st.write("**Personajes registrados:**")
                for p_name in info_m.get("personajes", {}).keys():
                    st.caption(f"• {p_name}")

# ====================== PESTAÑA 2: CHAT CON IA (CONECTADO) ======================
elif st.session_state.tab_activa == "Chat":
    st.markdown("### 💬 Chat & Rol Inmersivo")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("Crea un mundo y un personaje primero para chatear.")
    else:
        mundo_sel = st.selectbox("Selecciona el Mundo", mundos, key="c_mundo")
        personajes = list(st.session_state.data["mundos"][mundo_sel]["personajes"].keys())
        
        if not personajes:
            st.info("Este mundo no tiene personajes aún.")
        else:
            pers_sel = st.selectbox("Hablar con:", personajes, key="c_pers")
            p_data = st.session_state.data["mundos"][mundo_sel]["personajes"][pers_sel]
            
            # Tarjeta de estado del personaje
            params = p_data["parametros"]
            st.markdown(f"""
                <div class="app-card">
                    <h4 style="margin:0; color: #c7d2fe;">👤 {pers_sel}</h4>
                    <p style="font-size: 12px; color: #94a3b8; margin-top: 4px;">{p_data.get('descripcion', '')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💖 Romance", params["Romance"])
            c2.metric("🤝 Amistad", params["Amistad"])
            c3.metric("🛡️ Confianza", params["Confianza"])
            c4.metric("⚡ Odio", params["Odio"])
            
            st.markdown("---")
            
            if "chat" not in p_data:
                p_data["chat"] = []
                
            for m in p_data["chat"]:
                if m["rol"] == "usuario":
                    st.markdown(f"👤 **Tú:** {m['texto']}")
                else:
                    st.markdown(f"🤖 **{pers_sel}:** {m['texto']}")
                st.caption(f"[{m['hora']}]")
                st.markdown("---")
                
            with st.form("chat_form", clear_on_submit=True):
                user_input = st.text_area("Escribe tu acción o diálogo en la simulación:", placeholder="Ej: *Me acerco a Shoto en el pasillo de la U.A. y le ofrezco un jugo mientras hablamos del entrenamiento...*")
                enviar = st.form_submit_button("Enviar a la Simulación")
                
                if enviar and user_input.strip():
                    hora_act = datetime.now().strftime("%H:%M")
                    p_data["chat"].append({"rol": "usuario", "texto": user_input, "hora": hora_act})
                    
                    # Motor de IA contextual (Mundo + Personaje + Stats)
                    u_low = user_input.lower()
                    lore_m = st.session_state.data["mundos"][mundo_sel]["lore"]
                    
                    if params["Romance"] > 30 and ("jugo" in u_low or "cerca" in u_low or "sonrisa" in u_low):
                        respuesta = f"Observa la bebida por un segundo antes de tomarla con un ligero toque de sorpresa. Sus ojos heterocromáticos se fijan en ti y una leve calidez parece relajar su postura habitualmente seria: \"Gracias... No suelo prestar atención a estas cosas durante los descansos en la U.A., pero aprecio que te hayas tomado el tiempo. ¿Cómo va tu entrenamiento hoy?\""
                        params["Romance"] = min(100, params["Romance"] + 4)
                        params["Confianza"] = min(100, params["Confianza"] + 3)
                    elif params["Odio"] > 30 or "atacar" in u_low:
                        respuesta = f"Mantiene una distancia prudente, activando sutilmente una capa de hielo bajo sus pies mientras te mira fijamente con frialdad: \"No te acerques tanto. En un entorno como este ({mundo_sel}), no puedo darme el lujo de confiar a ciegas en cualquiera.\""
                        params["Odio"] = min(100, params["Odio"] + 5)
                    else:
                        respuesta = f"Se cruza de brazos y asiente con serenidad, analizando tus palabras en el contexto de la academia: \"Entiendo lo que dices. Las cosas en la U.A. se están volviendo más intensas cada día, así que es bueno tener a alguien con quien hablar con claridad sobre esto.\""
                        params["Amistad"] = min(100, params["Amistad"] + 3)
                        
                    p_data["chat"].append({"rol": "personaje", "texto": respuesta, "hora": hora_act})
                    guardar_datos(st.session_state.data)
                    st.rerun()

# ====================== PESTAÑA 3: APPS Y MÓDULOS DEL MUNDO ======================
elif st.session_state.tab_activa == "Apps":
    st.markdown("### ⚡ Apps Instaladas en tu Universo")
    st.caption("Estas aplicaciones ejecutan eventos especiales que alteran la historia y las relaciones.")
    
    mundos = list(st.session_state.data["mundos"].keys())
    if not mundos:
        st.warning("Crea un mundo primero.")
    else:
        m_app = st.selectbox("Mundo activo para ejecutar Apps", mundos)
        p_app = st.selectbox("Personaje objetivo", list(st.session_state.data["mundos"][m_app]["personajes"].keys()))
        
        st.markdown("#### 📱 Selecciona una App del Sistema:")
        
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown("""
                <div class="app-card">
                    🎯 <b>App: Entrenamiento / Combate</b>
                    <p style="font-size: 11px; color: #94a3b8;">Simula batallas o ejercicios de héroe y mide la confianza.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Ejecutar Combate", key="app_combate"):
                p_ref = st.session_state.data["mundos"][m_app]["personajes"][p_app]["parametros"]
                p_ref["Confianza"] = min(100, p_ref["Confianza"] + 10)
                p_ref["Amistad"] = min(100, p_ref["Amistad"] + 5)
                guardar_datos(st.session_state.data)
                st.success(f"⚔️ ¡Entrenamiento completado con {p_app}! Confianza y Amistad aumentaron.")
                st.rerun()
                
        with col_a2:
            st.markdown("""
                <div class="app-card">
                    💌 <b>App: Cita / Momento a Solas</b>
                    <p style="font-size: 11px; color: #94a3b8;">Invita al personaje a un evento fuera de clases.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Invitar a Salir", key="app_cita"):
                p_ref = st.session_state.data["mundos"][m_app]["personajes"][p_app]["parametros"]
                p_ref["Romance"] = min(100, p_ref["Romance"] + 12)
                guardar_datos(st.session_state.data)
                st.success(f"💖 ¡Compartieron un momento especial! El Romance con {p_app} subió +12.")
                st.rerun()

# ====================== PESTAÑA 4: CREAR MUNDOS Y PERSONAJES ======================
elif st.session_state.tab_activa == "Crear":
    st.markdown("### ⚙️ Creador de Universos y Fichas")
    
    opcion = st.radio("¿Qué deseas crear?", ["🌌 Nuevo Universo", "👤 Nuevo Personaje"])
    
    if opcion == "🌌 Nuevo Universo":
        with st.form("form_crear_u"):
            n_mundo = st.text_input("Nombre del Mundo (ej: My Hero Academia)")
            lore_u = st.text_area("Lore / Reglas / Contexto del Universo")
            if st.form_submit_button("Guardar Universo"):
                if n_mundo and n_mundo not in st.session_state.data["mundos"]:
                    st.session_state.data["mundos"][n_mundo] = {
                        "lore": lore_u,
                        "personajes": {},
                        "apps": ["Entrenamiento", "Cita", "Diario"]
                    }
                    guardar_datos(st.session_state.data)
                    st.success(f"¡Universo '{n_mundo}' creado exitosamente!")
                    st.rerun()
                else:
                    st.error("Nombre inválido o ya existente.")
                    
    elif opcion == "👤 Nuevo Personaje":
        mundos = list(st.session_state.data["mundos"].keys())
        if not mundos:
            st.warning("Crea un mundo primero.")
        else:
            m_target = st.selectbox("Asignar al mundo:", mundos)
            with st.form("form_crear_p"):
                n_pers = st.text_input("Nombre del Personaje")
                desc_p = st.text_area("Descripción física, personalidad y Quirk/Poderes")
                r = st.slider("Romance Inicial", 0, 100, 10)
                a = st.slider("Amistad Inicial", 0, 100, 20)
                c = st.slider("Confianza Inicial", 0, 100, 15)
                o = st.slider("Odio Inicial", 0, 100, 0)
                
                if st.form_submit_button("Guardar Personaje"):
                    if n_pers.strip():
                        st.session_state.data["mundos"][m_target]["personajes"][n_pers] = {
                            "descripcion": desc_p,
                            "parametros": {"Romance": r, "Amistad": a, "Confianza": c, "Odio": o},
                            "chat": []
                        }
                        guardar_datos(st.session_state.data)
                        st.success(f"¡{n_pers} registrado en {m_target}!")
                        st.rerun()
