
import streamlit as st
import random

st.set_page_config(
    page_title="Mundos | Universe OS",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- DISEÑO ----------
st.markdown("""
<style>
.stApp {
    background: #090e1b;
    color: #f4f6ff;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1050px;
    padding: 1.5rem 1.2rem 4rem;
}
h1, h2, h3, p, label {
    color: #f4f6ff;
}
.hero {
    background: linear-gradient(135deg, #202f62, #11182d 75%);
    border: 1px solid #536dfe;
    border-radius: 24px;
    padding: 26px;
    margin: 12px 0 24px;
}
.world-card {
    background: #111a2e;
    border: 1px solid #283b68;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}
.tag {
    color: #a9bbff;
    font-size: 12px;
    letter-spacing: 1px;
}
.stButton > button,
.stFormSubmitButton > button {
    background: #536dfe;
    color: white;
    border: 0;
    border-radius: 13px;
    min-height: 44px;
    width: 100%;
    font-weight: 600;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #7186ff;
    color: white;
    border: 0;
}
input, textarea {
    color: #f4f6ff !important;
}
div[data-testid="stChatMessage"] {
    background: #111a2e;
    border: 1px solid #283b68;
    border-radius: 16px;
}
hr {
    border-color: #283b68;
}
@media (max-width: 600px) {
    .block-container {
        padding: 1rem 0.7rem 3rem;
    }
    .hero {
        padding: 18px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- DATOS INICIALES ----------
if "mundos" not in st.session_state:
    st.session_state.mundos = [
        {
            "nombre": "My Hero Academia",
            "descripcion": "Una academia de héroes, nuevos amigos "
                           "y poderes extraordinarios.",
            "genero": "Aventura",
            "personaje": "Aizawa",
            "inicio": "Tu primer día en la academia",
        },
        {
            "nombre": "Reinos ocultos",
            "descripcion": "Un reino mágico lleno de secretos.",
            "genero": "Fantasía",
            "personaje": "La guardiana",
            "inicio": "El secreto del bosque",
        },
    ]

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

if "mundo_activo" not in st.session_state:
    st.session_state.mundo_activo = "My Hero Academia"

if "historias" not in st.session_state:
    st.session_state.historias = {}

if "chats" not in st.session_state:
    st.session_state.chats = {}

# ---------- FUNCIONES ----------
def buscar_mundo(nombre):
    for mundo in st.session_state.mundos:
        if mundo["nombre"] == nombre:
            return mundo
    return None


def abrir_historia(nombre):
    st.session_state.mundo_activo = nombre
    if nombre not in st.session_state.historias:
        mundo = buscar_mundo(nombre)
        if mundo:
            st.session_state.historias[nombre] = [
                "🌌 " + mundo["inicio"] + ". " + mundo["descripcion"]
            ]
    st.session_state.pagina = "Historia"


# ---------- CABECERA ----------
st.markdown("# 🌌 Universe OS")
st.caption("Tu universo. Tus personajes. Tus decisiones.")

paginas = [
    "Inicio", "Explorar", "Chats",
    "Crear mundo", "Comunidad", "Perfil"
]

st.radio(
    "Navegación",
    paginas,
    horizontal=True,
    label_visibility="collapsed",
    key="nav",
)
pagina = st.session_state.nav
st.session_state.pagina = pagina

# ---------- INICIO ----------
if pagina == "Inicio":
    st.markdown("""
    <div class="hero">
        <div class="tag">✦ TU ESPACIO CREATIVO</div>
        <h1>¿Qué historia vivirás hoy?</h1>
        <p>Crea universos, descubre personajes
        y escribe una aventura a tu manera.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✨ Crear mi primer mundo", key="crear_inicio"):
        st.session_state.pagina = "Crear mundo"
        st.rerun()

    st.markdown("## 🪐 Tus universos")

    if not st.session_state.mundos:
        st.info("Todavía no tienes mundos. ¡Crea el primero!")

    for i, mundo in enumerate(st.session_state.mundos):
        with st.container(border=True):
            st.markdown(f"### 🌠 {mundo['nombre']}")
            st.caption(mundo["genero"])
            st.write(mundo["descripcion"])
            if st.button(
                "▶ Abrir historia",
                key=f"inicio_{i}",
                use_container_width=True,
            ):
                abrir_historia(mundo["nombre"])
                st.rerun()

# ---------- EXPLORAR ----------
elif pagina == "Explorar":
    st.title("🔭 Explorar mundos")
    st.write("Elige un universo para entrar en su historia.")

    for i, mundo in enumerate(st.session_state.mundos):
        with st.container(border=True):
            st.markdown(f"### 🌌 {mundo['nombre']}")
            st.caption(f"Género: {mundo['genero']}")
            st.write(mundo["descripcion"])
            if st.button(
                "Entrar en este mundo",
                key=f"explorar_{i}",
                use_container_width=True,
            ):
                abrir_historia(mundo["nombre"])
                st.rerun()

# ---------- CREAR MUNDO ----------
elif pagina == "Crear mundo":
    st.title("✨ Crear un mundo")
    st.write("Dale forma a un universo propio.")

    with st.form("formulario_mundo"):
        nombre = st.text_input(
            "Nombre del mundo",
            placeholder="Ej. Academia de las estrellas",
        )
        descripcion = st.text_area(
            "Descripción",
            placeholder="¿Qué sucede en este universo?",
        )
        genero = st.selectbox(
            "Género",
            [
                "Fantasía", "Aventura", "Drama",
                "Misterio", "Ciencia ficción",
                "Romance", "Vida cotidiana",
            ],
        )
        personaje = st.text_input(
            "Personaje principal",
            placeholder="Ej. Alex, una estudiante nueva",
        )
        inicio = st.text_input(
            "Título del comienzo",
            value="Un nuevo comienzo",
        )
        enviar = st.form_submit_button(
            "🌌 Crear mundo",
            use_container_width=True,
        )

    if enviar:
        nombre = nombre.strip()
        nombres_existentes = [
            m["nombre"].casefold() for m in st.session_state.mundos
        ]

        if not nombre:
            st.warning("Primero escribe el nombre del mundo.")
        elif nombre.casefold() in nombres_existentes:
            st.warning("Ya existe un mundo con ese nombre.")
        else:
            mundo = {
                "nombre": nombre,
                "descripcion": descripcion.strip()
                    or "Una aventura por descubrir.",
                "genero": genero,
                "personaje": personaje.strip() or "Personaje misterioso",
                "inicio": inicio.strip() or "Un nuevo comienzo",
            }
            st.session_state.mundos.append(mundo)
            abrir_historia(nombre)
            st.success(f"¡El mundo «{nombre}» está creado!")
            st.rerun()

# ---------- HISTORIA INTERACTIVA ----------
elif pagina == "Historia":
    mundo = buscar_mundo(st.session_state.mundo_activo)

    if not mundo:
        st.warning("No encontramos ese mundo.")
        if st.button("Volver al inicio"):
            st.session_state.pagina = "Inicio"
            st.rerun()
    else:
        st.title(f"📖 {mundo['nombre']}")
        st.caption(
            f"{mundo['genero']} · Protagonista: {mundo['personaje']}"
        )

        historia = st.session_state.historias.setdefault(
            mundo["nombre"],
            [mundo["inicio"] + ". " + mundo["descripcion"]],
        )

        for entrada in historia:
            st.markdown(
                f'<div class="world-card">{entrada}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("### ¿Qué decides hacer?")

        opciones = [
            "🔎 Explorar el lugar",
            "💬 Hablar con un personaje",
            "⚡ Tomar una decisión arriesgada",
        ]

        respuestas = {
            opciones[0]: [
                "Descubres una pista inesperada. Parece que "
                "este lugar esconde algo importante.",
                "Encuentras un camino nuevo que podría cambiar "
                "tu aventura.",
            ],
            opciones[1]: [
                f"{mundo['personaje']} te mira con curiosidad. "
                "«Quiero saber más de ti. ¿Qué te trae por aquí?»",
                f"{mundo['personaje']} te saluda. "
                "«Hay algo que deberías descubrir antes de continuar»",
            ],
            opciones[2]: [
                "Tu decisión sorprende a todos. Se abre una "
                "nueva posibilidad en la historia.",
                "El ambiente cambia. Tu aventura toma un rumbo "
                "que nadie esperaba.",
            ],
        }

        columnas = st.columns(3)
        for i, opcion in enumerate(opciones):
            with columnas[i]:
                if st.button(opcion, key=f"opcion_{i}"):
                    texto = random.choice(respuestas[opcion])
                    historia.append(texto)
                    st.rerun()

        if st.button("↩ Volver al inicio"):
            st.session_state.pagina = "Inicio"
            st.rerun()

# ---------- CHATS ----------
elif pagina == "Chats":
    st.title("💬 Conversaciones")
    st.caption("Habla con los personajes de tus universos.")

    nombres = [m["nombre"] for m in st.session_state.mundos]
    if nombres:
        elegido = st.selectbox(
            "Selecciona un mundo",
            nombres,
            index=(
                nombres.index(st.session_state.mundo_activo)
                if st.session_state.mundo_activo in nombres else 0
            ),
        )
        mundo = buscar_mundo(elegido)
        personaje = mundo["personaje"]

        clave = f"{elegido}:{personaje}"
        mensajes = st.session_state.chats.setdefault(
            clave,
            [{
                "rol": "assistant",
                "texto": f"¡Hola! Soy {personaje}. "
                         "¿Qué aventura te gustaría vivir?"
            }],
        )

        st.markdown(f"### 🎭 {personaje}")
        for mensaje in mensajes:
            with st.chat_message(mensaje["rol"]):
                st.write(mensaje["texto"])

        entrada = st.chat_input("Escribe tu mensaje...")
        if entrada:
            mensajes.append({"rol": "user", "texto": entrada})
            mensajes.append({
                "rol": "assistant",
                "texto": (
                    f"{personaje} escucha tu mensaje: «{entrada}». "
                    "¡Cuéntame más para continuar nuestra aventura!"
                ),
            })
            st.rerun()
    else:
        st.info("Crea un mundo antes de empezar a conversar.")

# ---------- COMUNIDAD ----------
elif pagina == "Comunidad":
    st.title("👥 Comunidad")
    st.write("Tus mundos disponibles en esta versión.")

    for mundo in st.session_state.mundos:
        with st.container(border=True):
            st.markdown(f"### 🌍 {mundo['nombre']}")
            st.caption(mundo["genero"])
            st.write(mundo["descripcion"])

# ---------- PERFIL ----------
elif pagina == "Perfil":
    st.title("👤 Mi perfil")
    st.write("Tu espacio personal de creación.")
    st.metric("Mundos creados", len(st.session_state.mundos))
    st.metric(
        "Historias iniciadas",
        len(st.session_state.historias),
    )
    st.caption(
        "Esta versión guarda tus cambios durante la sesión actual."
    )

st.divider()
st.caption("Universe OS · Una pequeña idea puede crear un universo.")
