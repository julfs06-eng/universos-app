
import streamlit as st
import json
import os
import random
import uuid

st.set_page_config(
    page_title="Universe OS",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DB_FILE = "universos.json"

# ---------- ESTILO ----------
st.markdown("""
<style>
.stApp {
    background: #090b14;
    color: #f3f3ff;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1050px;
    padding: 1.5rem 1rem 4rem;
}
h1, h2, h3, p, label {
    color: #f3f3ff;
}
.hero {
    background: linear-gradient(135deg,#27265b,#111426 75%);
    border: 1px solid #6556db;
    border-radius: 24px;
    padding: 25px;
    margin: 12px 0 22px;
}
.panel {
    background: #111525;
    border: 1px solid #29314c;
    border-radius: 18px;
    padding: 17px;
    margin: 8px 0;
}
.small {
    color: #a9b3da;
    font-size: 12px;
    letter-spacing: 1px;
}
.stButton > button,
.stFormSubmitButton > button {
    background: #6857e8;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 42px;
    width: 100%;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #8274ff;
    color: white;
    border: 0;
}
[data-testid="stChatMessage"] {
    background: #13182a;
    border: 1px solid #29314c;
    border-radius: 14px;
}
hr {
    border-color: #29314c;
}
</style>
""", unsafe_allow_html=True)

# ---------- ESTADO Y DATOS ----------
def cargar_mundos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return [
        {
            "id": "demo_mha",
            "nombre": "My Hero Academia",
            "descripcion": "Una academia de héroes y poderes extraordinarios.",
            "genero": "Anime / Aventura",
            "personajes": [
                {"nombre": "Aizawa", "rol": "Profesor", "personalidad": "Serio y observador"}
            ],
            "inicio": "Tu primer día en la academia",
            "instrucciones": "Respeta la personalidad de cada personaje.",
            "apps": ["Historias", "Personajes", "Chats"],
            "historia": [
                "Llegas a la academia. Una nueva etapa de tu vida está a punto de comenzar."
            ],
            "chats": {},
        }
    ]


if "mundos" not in st.session_state:
    st.session_state.mundos = cargar_mundos()

if "nav" not in st.session_state:
    st.session_state.nav = "Inicio"

if "mundo_id" not in st.session_state:
    st.session_state.mundo_id = st.session_state.mundos[0]["id"]

if "paso" not in st.session_state:
    st.session_state.paso = 0

if "borrador" not in st.session_state:
    st.session_state.borrador = {}

if "personajes_draft" not in st.session_state:
    st.session_state.personajes_draft = []


def guardar_mundos():
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(
                st.session_state.mundos,
                f,
                ensure_ascii=False,
                indent=2,
            )
        return True
    except OSError:
        return False


def avisar_guardado():
    if not guardar_mundos():
        st.warning(
            "No se pudo guardar el archivo local. "
            "Descarga o copia tus datos importantes."
        )


def mundo_actual():
    for m in st.session_state.mundos:
        if m["id"] == st.session_state.mundo_id:
            return m
    return None


def ir(pagina):
    st.session_state.nav = pagina
    st.rerun()


def abrir_mundo(m):
    st.session_state.mundo_id = m["id"]
    ir("Historia")


def tarjeta_mundo(m, prefijo):
    with st.container(border=True):
        st.markdown(f"### 🌌 {m['nombre']}")
        st.caption(m["genero"])
        st.write(m["descripcion"])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("▶ Abrir", key=f"{prefijo}_open_{m['id']}"):
                abrir_mundo(m)
        with c2:
            if st.button("⚙ Configurar", key=f"{prefijo}_edit_{m['id']}"):
                st.session_state.mundo_id = m["id"]
                ir("Apps")


# ---------- CABECERA ----------
st.markdown("# 🌌 Universe OS")
st.caption("Crea universos. Diseña personajes. Vive historias.")

paginas = ["Inicio", "Mundos", "Crear mundo", "Historia", "Chats", "Apps"]
st.radio(
    "Navegación",
    paginas,
    horizontal=True,
    key="nav",
    label_visibility="collapsed",
)

# ---------- INICIO ----------
if st.session_state.nav == "Inicio":
    st.markdown("""
    <div class="hero">
      <div class="small">TU UNIVERSO PERSONAL</div>
      <h1>¿Qué historia vas a crear?</h1>
      <p>Un espacio para construir mundos, personajes y aventuras.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with a:
        if st.button("✨ Crear mundo"):
            st.session_state.paso = 0
            st.session_state.borrador = {}
            st.session_state.personajes_draft = []
            ir("Crear mundo")
    with b:
        if st.button("📚 Mis mundos"):
            ir("Mundos")
    with c:
        if st.button("💬 Conversaciones"):
            ir("Chats")

    st.markdown("## ✦ Continuar explorando")
    for m in st.session_state.mundos:
        tarjeta_mundo(m, "home")

# ---------- MUNDOS ----------
elif st.session_state.nav == "Mundos":
    st.title("🪐 Mis mundos")
    if st.button("＋ Crear un universo"):
        st.session_state.paso = 0
        st.session_state.borrador = {}
        st.session_state.personajes_draft = []
        ir("Crear mundo")

    if not st.session_state.mundos:
        st.info("Todavía no hay mundos creados.")
    for m in st.session_state.mundos:
        tarjeta_mundo(m, "worlds")

# ---------- ASISTENTE DE CREACIÓN ----------
elif st.session_state.nav == "Crear mundo":
    st.title("✨ Crear un mundo")

    pasos = [
        "1. Básicos",
        "2. Personajes",
        "3. Inicio",
        "4. Apps",
        "5. Instrucciones",
    ]
    st.progress((st.session_state.paso + 1) / len(pasos))
    st.caption("  /  ".join(pasos))
    paso = st.session_state.paso
    d = st.session_state.borrador

    if paso == 0:
        st.subheader("🌍 Los datos de tu universo")
        with st.form("basicos"):
            nombre = st.text_input(
                "Nombre del mundo",
                value=d.get("nombre", ""),
            )
            descripcion = st.text_area(
                "¿De qué trata?",
                value=d.get("descripcion", ""),
            )
            genero = st.selectbox(
                "Género",
                ["Anime", "Fantasía", "Aventura", "Drama",
                 "Misterio", "Ciencia ficción", "Vida cotidiana",
                 "Romance", "Otro"],
                index=0,
            )
            ok = st.form_submit_button("Siguiente →")
        if ok:
            if not nombre.strip():
                st.warning("Ponle un nombre al mundo.")
            else:
                d.update({
                    "nombre": nombre.strip(),
                    "descripcion": descripcion.strip(),
                    "genero": genero,
                })
                st.session_state.paso = 1
                st.rerun()

    elif paso == 1:
        st.subheader("🎭 Diseña tus personajes")
        st.write("Puedes añadir varios personajes a tu universo.")

        with st.form("personaje_nuevo", clear_on_submit=True):
            pnombre = st.text_input("Nombre del personaje")
            rol = st.text_input("Rol", placeholder="Ej. Profesor, rival, amiga")
            personalidad = st.text_area(
                "Personalidad",
                placeholder="Ej. Reservado, amable, competitivo...",
            )
            anadir = st.form_submit_button("＋ Añadir personaje")
        if anadir:
            if pnombre.strip():
                st.session_state.personajes_draft.append({
                    "nombre": pnombre.strip(),
                    "rol": rol.strip() or "Personaje",
                    "personalidad": personalidad.strip() or "Por definir",
                })
                st.rerun()
            else:
                st.warning("Escribe el nombre del personaje.")

        for i, p in enumerate(st.session_state.personajes_draft):
            with st.container(border=True):
                st.markdown(f"**{p['nombre']}** · {p['rol']}")
                st.write(p["personalidad"])
                if st.button("Eliminar", key=f"del_p_{i}"):
                    st.session_state.personajes_draft.pop(i)
                    st.rerun()

        x, y = st.columns(2)
        with x:
            if st.button("← Anterior"):
                st.session_state.paso = 0
                st.rerun()
        with y:
            if st.button("Siguiente →"):
                d["personajes"] = st.session_state.personajes_draft
                st.session_state.paso = 2
                st.rerun()

    elif paso == 2:
        st.subheader("📖 El comienzo de la historia")
        with st.form("inicio_historia"):
            inicio = st.text_input(
                "Título de la primera escena",
                value=d.get("inicio", "Un nuevo comienzo"),
            )
            escena = st.text_area(
                "¿Qué está pasando al empezar?",
                value=d.get("escena", ""),
                placeholder="Describe el lugar, el momento y la situación inicial...",
            )
            ok = st.form_submit_button("Siguiente →")
        if ok:
            d["inicio"] = inicio.strip() or "Un nuevo comienzo"
            d["escena"] = escena.strip()
            st.session_state.paso = 3
            st.rerun()
        if st.button("← Anterior"):
            st.session_state.paso = 1
            st.rerun()

    elif paso == 3:
        st.subheader("🧩 Aplicaciones del mundo")
        st.write("Elige las herramientas que quieres tener disponibles.")
        opciones = [
            "Historias", "Personajes", "Chats",
            "Diario", "Misiones", "Galería",
        ]
        seleccionadas = st.multiselect(
            "Apps instaladas",
            opciones,
            default=d.get("apps", ["Historias", "Personajes", "Chats"]),
        )
        d["apps"] = seleccionadas

        x, y = st.columns(2)
        with x:
            if st.button("← Anterior"):
                st.session_state.paso = 2
                st.rerun()
        with y:
            if st.button("Siguiente →"):
                st.session_state.paso = 4
                st.rerun()

    elif paso == 4:
        st.subheader("📜 Instrucciones del universo")
        instrucciones = st.text_area(
            "Reglas para narrar este mundo",
            value=d.get("instrucciones", ""),
            placeholder="Ej. Mantén la personalidad de los personajes, "
                        "recuerda las decisiones y usa diálogos...",
            height=160,
        )
        d["instrucciones"] = instrucciones

        st.markdown("### Vista previa")
        st.markdown(f"**{d.get('nombre', 'Mi mundo')}**")
        st.write(d.get("descripcion", "Sin descripción"))
        st.caption(d.get("genero", "Sin género"))
        st.write("Personajes:", len(st.session_state.personajes_draft))
        st.write("Apps:", ", ".join(d.get("apps", [])) or "Ninguna")

        x, y = st.columns(2)
        with x:
            if st.button("← Anterior"):
                st.session_state.paso = 3
                st.rerun()
        with y:
            if st.button("🌌 Crear universo"):
                nombre = d.get("nombre", "").strip()
                existe = any(
                    m["nombre"].casefold() == nombre.casefold()
                    for m in st.session_state.mundos
                )
                if not nombre:
                    st.error("El mundo necesita un nombre.")
                elif existe:
                    st.error("Ya existe un mundo con ese nombre.")
                else:
                    m = {
                        "id": str(uuid.uuid4()),
                        "nombre": nombre,
                        "descripcion": d.get("descripcion", ""),
                        "genero": d.get("genero", "Otro"),
                        "personajes": st.session_state.personajes_draft[:],
                        "inicio": d.get("inicio", "Un nuevo comienzo"),
                        "escena": d.get("escena", ""),
                        "instrucciones": instrucciones,
                        "apps": d.get("apps", []),
                        "historia": [
                            d.get("escena", "").strip()
                            or "Tu aventura acaba de comenzar."
                        ],
                        "chats": {},
                    }
                    st.session_state.mundos.append(m)
                    st.session_state.mundo_id = m["id"]
                    avisar_guardado()
                    st.session_state.borrador = {}
                    st.session_state.personajes_draft = []
                    st.session_state.paso = 0
                    st.success("¡Universo creado!")
                    ir("Historia")

# ---------- HISTORIA ----------
elif st.session_state.nav == "Historia":
    m = mundo_actual()
    if not m:
        st.info("Primero selecciona o crea un mundo.")
        if st.button("Ir a mis mundos"):
            ir("Mundos")
    else:
        st.title("📖 " + m["nombre"])
        st.caption(m["genero"] + " · Historia interactiva")

        if "Historias" not in m.get("apps", []):
            st.info("La app Historias no está activada en este universo.")
        else:
            for texto in m.get("historia", []):
                st.markdown(
                    f'<div class="panel">{texto}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("### ¿Qué haces ahora?")
            opciones = [
                "🔎 Explorar el entorno",
                "💬 Hablar con un personaje",
                "⚡ Tomar una decisión arriesgada",
            ]
            resultados = {
                opciones[0]: "Encuentras una pista que podría cambiar tu aventura.",
                opciones[1]: "Un personaje se acerca y te pregunta qué necesitas.",
                opciones[2]: "Tu decisión cambia el rumbo de la historia.",
            }
            cols = st.columns(3)
            for i, opcion in enumerate(opciones):
                with cols[i]:
                    if st.button(opcion, key=f"hist_{i}"):
                        m["historia"].append(resultados[opcion])
                        avisar_guardado()
                        st.rerun()

            if st.button("↻ Reiniciar historia"):
                m["historia"] = [
                    m.get("escena", "").strip()
                    or "Tu aventura acaba de comenzar."
                ]
                avisar_guardado()
                st.rerun()

# ---------- CHATS ----------
elif st.session_state.nav == "Chats":
    st.title("💬 Chats de personajes")
    m = mundo_actual()

    if not m:
        st.info("Crea un mundo primero.")
    elif "Chats" not in m.get("apps", []):
        st.info("Activa la app Chats en la configuración del mundo.")
    elif not m.get("personajes"):
        st.info("Este mundo aún no tiene personajes.")
    else:
        nombres = [p["nombre"] for p in m["personajes"]]
        elegido = st.selectbox("Conversar con", nombres)
        personaje = next(p for p in m["personajes"]
                         if p["nombre"] == elegido)
        clave = elegido
        mensajes = m.setdefault("chats", {}).setdefault(
            clave,
            [{
                "role": "assistant",
                "text": f"Hola, soy {elegido}. ¿Cómo comienza tu historia?"
            }],
        )

        st.caption(personaje.get("rol", "Personaje"))
        st.write(personaje.get("personalidad", ""))

        for msg in mensajes:
            with st.chat_message(msg["role"]):
                st.write(msg["text"])

        entrada = st.chat_input("Escribe un mensaje...")
        if entrada:
            mensajes.append({"role": "user", "text": entrada})
            mensajes.append({
                "role": "assistant",
                "text": (
                    f"{elegido} responde a tu mensaje: "
                    f"«{entrada}». ¿Qué decides hacer ahora?"
                ),
            })
            avisar_guardado()
            st.rerun()

# ---------- APPS Y CONFIGURACIÓN ----------
elif st.session_state.nav == "Apps":
    st.title("⚙️ Apps y configuración")
    m = mundo_actual()

    if not m:
        st.info("Selecciona un mundo primero.")
    else:
        st.markdown(f"### 🌌 {m['nombre']}")
        st.write(m["descripcion"])

        opciones = [
            "Historias", "Personajes", "Chats",
            "Diario", "Misiones", "Galería",
        ]
        activas = st.multiselect(
            "Aplicaciones instaladas",
            opciones,
            default=m.get("apps", []),
        )
        instrucciones = st.text_area(
            "Instrucciones del mundo",
            value=m.get("instrucciones", ""),
        )

        if st.button("💾 Guardar configuración"):
            m["apps"] = activas
            m["instrucciones"] = instrucciones
            avisar_guardado()
            st.success("Configuración actualizada.")

        st.markdown("### Personajes")
        for p in m.get("personajes", []):
            with st.container(border=True):
                st.markdown(f"**{p['nombre']}** · {p['rol']}")
                st.write(p["personalidad"])

st.divider()
st.caption(
    "UNIVERSE OS · Prototipo gratuito. "
    "Las respuestas de personajes aún no usan una IA real."
)


       
        