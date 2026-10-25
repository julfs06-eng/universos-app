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

# Control de navegación estilo OS (Escritorio de apps vs Aplicación abierta)
if "current_app" not in st.session_state:
    st.session_state.current_app = "Home"

# Barra superior estilo barra de estado de celular
col_s1, col_s2, col_s3 = st.columns([2, 6, 2])
with col_s1:
    st.caption("📶 5G  🔋 100%")
with col_s2:
    st.markdown("<p style='text-align: center; margin: 0; font-size: 14px;'><b>UNIVERSE MOBILE OS</b></p>", unsafe_allow_html=True)
with col_s3:
    current_time = datetime.now().strftime("%H:%M")
    st.caption(f"🕒 {current_time}")

st.markdown("---")

# ====================== PANTALLA DE INICIO (HOME / ESCRITORIO DE APPS) ======================
if st.session_state.current_app == "Home":
    st.markdown("### 📱 Pantalla Principal")
    st.write("Selecciona una aplicación para iniciar la simulación:")
    
    # Cuadrícula de aplicaciones estilo teléfono
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌌\n\n**Gestor de Mundos**\nCrear y explorar universos", use_container_width=True):
            st.session_state.current_app = "Mundos"
            st.rerun()
            
        if st.button("👥\n\n**Directorio / Personajes**\nCrear y editar avatares", use_container_width=True):
            st.session_state.current_app = "Personajes"
            st.rerun()

    with col2:
        if st.button("💬\n\n**Mensajes (Chat)**\nRol inmersivo avanzado", use_container_width=True):
            st.session_state.current_app = "Chat"
            st.rerun()
            
        if st.button("⚡\n\n**Simulador de Acciones**\nEventos y consecuencias", use_container_width=True):
            st.session_state.current_app = "Acciones"
            st.rerun()

# ====================== APP 1: GESTOR DE MUNDOS ======================
elif st.session_state.current_app == "Mundos":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
        
    st.subheader("🌌 Gestor de Universos (Lore)")
    
    with st.form("form_mundo_os"):
        nombre_mundo = st.text_input("Nombre del mundo (ej: My Hero Academia)")
        lore = st.text_area("Historia / Lore del mundo (Reglas, ambiente, contexto)")
        crear = st.form_submit_button("Crear Universo")
        
        if crear and nombre_mundo.strip():
            if nombre_mundo in st.session_state.data["mundos"]:
                st.error("⚠️ Este mundo ya existe.")
            else:
                st.session_state.data["mundos"][nombre_mundo] = {
                    "lore": lore,
                    "personajes": {},
                    "bitacora": []
                }
                guardar_datos(st.session_state.data)
                st.success(f"🚀 Mundo '{nombre_mundo}' creado con éxito.")
                st.rerun()
                
    st.markdown("---")
    st.markdown("### 🌍 Mundos Registrados")
    if not st.session_state.data["mundos"]:
        st.info("No hay mundos creados aún.")
    else:
        for m_name, m_info in st.session_state.data["mundos"].items():
            with st.expander(f"Universo: {m_name}"):
                st.write(f"**Lore:** {m_info.get('lore', '')}")
                st.write(f"**Personajes:** {len(m_info.get('personajes', {}))}")

# ====================== APP 2: GESTOR DE PERSONAJES E IMÁGENES ======================
elif st.session_state.current_app == "Personajes":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
        
    st.subheader("👥 Creación de Personajes y Avatares")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("⚠️ Primero debes crear un mundo en la app de Mundos.")
    else:
        mundo_sel = st.selectbox("Mundo destino", mundos)
        
        with st.form("form_pers_os"):
            nombre_pers = st.text_input("Nombre del personaje")
            desc_pers = st.text_area("Descripción física y psicológica, poderes o quirks")
            
            # Opción para subir imagen o avatar personalizado
            st.markdown("### 🖼️ Imagen / Avatar del Personaje")
            img_url = st.text_input("URL de imagen opcional (o pega un link de imagen web)")
            
            st.markdown("### 🎚️ Parámetros Iniciales")
            c1, c2 = st.columns(2)
            with c1:
                romance = st.slider("Romance", 0, 100, 10)
                amistad = st.slider("Amistad", 0, 100, 20)
            with c2:
                confianza = st.slider("Confianza", 0, 100, 15)
                odio = st.slider("Odio", 0, 100, 0)
                
            guardar_p = st.form_submit_button("Guardar Personaje en el Sistema")
            
            if guardar_p and nombre_pers.strip():
                st.session_state.data["mundos"][mundo_sel]["personajes"][nombre_pers] = {
                    "descripcion": desc_pers,
                    "imagen": img_url,
                    "parametros": {
                        "Romance": romance,
                        "Amistad": amistad,
                        "Confianza": confianza,
                        "Odio": odio
                    },
                    "chat": []
                }
                guardar_datos(st.session_state.data)
                st.success(f"✨ Personaje '{nombre_pers}' guardado correctamente.")
                st.rerun()

# ====================== APP 3: CHAT INMERSIVO AVANZADO ======================
elif st.session_state.current_app == "Chat":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
        
    st.subheader("💬 Mensajes / Chat Inmersivo")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("No hay mundos creados.")
    else:
        mundo_c = st.selectbox("Seleccionar Mundo", mundos, key="chat_m")
        personajes_c = list(st.session_state.data["mundos"][mundo_c]["personajes"].keys())
        
        if not personajes_c:
            st.info("Este mundo no tiene personajes.")
        else:
            pers_c = st.selectbox("Seleccionar Conversación", personajes_c, key="chat_p")
            datos_p = st.session_state.data["mundos"][mundo_c]["personajes"][pers_c]
            
            # Mostrar imagen del personaje si subió o puso URL
            if datos_p.get("imagen"):
                st.image(datos_p["imagen"], width=120)
                
            st.markdown(f"**Estado vincular con {pers_c}:**")
            p = datos_p["parametros"]
            cols_m = st.columns(4)
            cols_m[0].metric("Romance", p["Romance"])
            cols_m[1].metric("Amistad", p["Amistad"])
            cols_m[2].metric("Confianza", p["Confianza"])
            cols_m[3].metric("Odio", p["Odio"])
            
            st.markdown("---")
            
            if "chat" not in datos_p:
                datos_p["chat"] = []
                
            # Historial de mensajes estilo app de mensajería
            for msg in datos_p["chat"]:
                if msg["rol"] == "usuario":
                    st.markdown(f"👤 **Tú:** {msg['texto']}")
                else:
                    st.markdown(f"🤖 **{pers_c}:** {msg['texto']}")
                st.caption(f"[{msg['hora']}]")
                st.markdown("---")
                
            with st.form(key="chat_msg_form", clear_on_submit=True):
                texto_u = st.text_area("Escribe tu acción o mensaje detallado:")
                enviar_m = st.form_submit_button("Enviar Mensaje")
                
                if enviar_m and texto_u.strip():
                    hora_act = datetime.now().strftime("%H:%M")
                    datos_p["chat"].append({"rol": "usuario", "texto": texto_u, "hora": hora_act})
                    
                    # Generador de respuesta larga, descriptiva y con memoria de parámetros
                    txt_lower = texto_u.lower()
                    if p["Odio"] > 40 or "atacar" in txt_lower:
                        respuesta = f"Retrocede un paso con una mirada fría y distante, cruzando los brazos mientras analiza cada movimiento tuyo. Con un tono cortante y serio, responde: \"No finjas que te importa lo que pasa aquí. Las reglas de {mundo_c} no perdonan errores, y yo tampoco.\""
                        p["Odio"] = min(100, p["Odio"] + 5)
                    elif p["Romance"] > 35 or "lindo" in txt_lower or "abrazo" in txt_lower:
                        respuesta = f"Un rubor leve se asoma por su rostro mientras aparta la mirada con algo de timidez, intentando mantener la compostura. Su voz baja de tono, volviéndose más suave: \"Es extraño... normalmente no suelo confiar en nadie en este lugar, pero contigo las cosas se sienten diferentes. Gracias por estar aquí.\""
                        p["Romance"] = min(100, p["Romance"] + 6)
                    else:
                        respuesta = f"Exhala un suspiro pausado, observando el entorno antes de responder con atención a tus palabras: \"Entiendo perfectamente a qué te refieres. Entre los peligros de {mundo_c} y todo lo que tenemos pendiente, tenemos que ser muy cuidadosos con cada paso que damos.\""
                        p["Amistad"] = min(100, p["Amistad"] + 4)
                        
                    datos_p["chat"].append({"rol": "personaje", "texto": respuesta, "hora": hora_act})
                    guardar_datos(st.session_state.data)
                    st.rerun()

# ====================== APP 4: ACCIONES DINÁMICAS ======================
elif st.session_state.current_app == "Acciones":
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_app = "Home"
        st.rerun()
        
    st.subheader("⚡ Simulador de Acciones y Consecuencias")
    mundos = list(st.session_state.data["mundos"].keys())
    
    if not mundos:
        st.warning("No hay mundos creados.")
    else:
        mundo_a = st.selectbox("Mundo activo", mundos, key="act_m")
        personajes_a = list(st.session_state.data["mundos"][mundo_a]["personajes"].keys())
        
        if not personajes_a:
            st.info("No hay personajes en este mundo.")
        else:
            pers_a = st.selectbox("Personaje involucrado", personajes_a, key="act_p")
            accion_txt = st.text_area("Describe la acción o evento que realizas con el personaje:", placeholder="Ej: Lo defendí de un peligro inminente y compartimos un momento a solas...")
            
            if st.button("Ejecutar Evento en la Historia"):
                if accion_txt.strip():
                    datos_act = st.session_state.data["mundos"][mundo_a]["personajes"][pers_a]
                    params_act = datos_act["parametros"]
                    
                    act_lower = accion_txt.lower()
                    if any(w in act_lower for w in ["salvar", "defender", "proteger", "ayudar"]):
                        params_act["Confianza"] = min(100, params_act["Confianza"] + 15)
                        params_act["Amistad"] = min(100, params_act["Amisted"] if "Amisted" in params_act else params_act["Amistad"] + 10)
                        resultado_str = "🛡️ ¡Impacto positivo! Confianza y Amistad aumentaron de forma notable."
                    elif any(w in act_lower for w in ["atacar", "traicionar", "insultar"]):
                        params_act["Odio"] = min(100, params_act["Odio"] + 20)
                        params_act["Confianza"] = max(0, params_act["Confianza"] - 15)
                        resultado_str = "⚡ ¡Impacto negativo! El Odio creció y la Confianza cayó."
                    else:
                        params_act["Amistad"] = min(100, params_act["Amistad"] + 5)
                        resultado_str = "📈 El evento transcurrió de manera neutral."
                        
                    guardar_datos(st.session_state.data)
                    st.success("¡Acción procesada por el sistema operativo!")
                    st.write(f"**Resultado:** {resultado_str}")
                    
                    st.markdown("#### Nuevos parámetros:")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Romance", params_act["Romance"])
                    c2.metric("Amistad", params_act["Amistad"])
                    c3.metric("Confianza", params_act["Confianza"])
                    c4.metric("Odio", params_act["Odio"])
                else:
                    st.warning("Escribe una acción primero.")

st.markdown("---")
st.caption("Universe Simulator OS - Interfaz Móvil v4.0")
                        
