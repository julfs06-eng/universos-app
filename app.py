
import json
import os
import uuid
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Universe OS",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DB_FILE = "universos.json"
GEMINI_MODEL = "gemini-2.5-flash"


# ---------- DISEÑO ----------
st.markdown("""
<style>
.stApp { background: #090b14; color: #f3f3ff; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1050px; padding: 1.3rem 1rem 4rem; }
h1, h2, h3, p, label { color: #f3f3ff; }
.hero {
    background: linear-gradient(135deg, #29265d, #111426);
    border: 1px solid #6556db;
    border-radius: 22px;
    padding: 24px;
    margin: 14px 0 22px;
}
.stButton > button, .stFormSubmitButton > button {
    background: #6857e8;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 42px;
    width: 100%;
    font-weight: 600;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #8274ff;
    color: white;
    border: 0;
}
[data-testid="stChatMessage"] {
    background: #13182a;
    border: 1px solid #29314c;
    border-radius: 14px;
}
hr { border-color: #29314c; }
</style>
""", unsafe_allow_html=True)


# ---------- DATOS ----------
def mundos_iniciales():
    return [{
        "id": "mha-demo",
        "nombre": "My Hero Academia",
        "descripcion": "Una academia de héroes, nuevos amigos y poderes extraordinarios.",
        "genero": "Anime / Aventura",
        "personajes": [{
            "id": str(uuid.uuid4()),
            "nombre": "Aizawa",
            "rol": "Profesor",
            "personalidad": "Serio, observador y exigente."
        }],
        "inicio": "Tu primer día en la academia",
        "escena": "Llegas a la academia. Una nueva aventura está a punto de comenzar.",
        "instrucciones": "Mantén la personalidad de cada personaje.",
        "apps": ["Historias", "Personajes", "Chats"],
        "historia": [
            "Llegas a la academia. Una nueva etapa de tu vida comienza."
        ],
        "chats": {}
    }]


def cargar_mundos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if isinstance(datos, list):
                return datos
        except (OSError, json.JSONDecodeError):
            pass
    return mundos_iniciales()


if "mundos" not in st.session_state:
    st.session_state.mundos = cargar_mundos()

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

if "mundo_id" not in st.session_state:
    st.session_state.mundo_id = (
        st.session_state.mundos[0]["id"]
        if st.session_state.mundos else None
    )

if "paso" not in st.session_state:
    st.session_state.paso = 0

if "borrador" not in st.session_state:
    st.session_state.borrador = {}

if "personajes_draft" not in st.session_state:
    st.session_state.personajes_draft = []


# ---------- FUNCIONES ----------
def guardar_mundos():
    try:
        with open(DB_FILE, "w", encoding="utf-8") as archivo:
            json.dump(
                st.session_state.mundos,
                archivo,
                ensure_ascii=False,
                indent=2
            )
        return True
    except (OSError, TypeError):
        return False


def guardar_y_avisar():
    if not guardar_mundos():
        st.warning(
            "No se pudieron guardar los datos en el archivo local. "
            "Streamlit Cloud no garantiza que este archivo permanezca "
            "tras todos los reinicios."
        )


def ir_a(pagina):
    st.session_state.pagina = pagina
    st.rerun()


def obtener_mundo(mundo_id=None):
    buscado = mundo_id or st.session_state.mundo_id
    for mundo in st.session_state.mundos:
        if mundo.get("id") == buscado:
            return mundo
    return None


def abrir_mundo(mundo):
    st.session_state.mundo_id = mundo["id"]
    if not mundo.get("historia"):
        mundo["historia"] = [
            mundo.get("escena") or "Tu aventura acaba de comenzar."
        ]
    ir_a("Historia")


def preparar_creador():
    st.session_state.paso = 0
    st.session_state.borrador = {}
    st.session_state.personajes_draft = []
    ir_a("Crear mundo")


def tarjeta_mundo(mundo, prefijo):
    with st.container(border=True):
        st.markdown("### 🌌 " + mundo.get("nombre", "Mundo sin nombre"))
        st.caption(mundo.get("genero", "Sin género"))
        st.write(mundo.get("descripcion", "Sin descripción"))

        c1, c2 = st.columns(2)

        with c1:
            if st.button(
                "▶ Abrir",
                key=f"{prefijo}_abrir_{mundo['id']}"
            ):
                abrir_mundo(mundo)

        with c2:
            if st.button(
                "⚙ Configurar",
                key=f"{prefijo}_config_{mundo['id']}"
            ):
                st.session_state.mundo_id = mundo["id"]
                ir_a("Apps")


# ---------- GEMINI ----------
def obtener_cliente_gemini():
    try:
        clave = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        clave = ""

    if not clave or not str(clave).strip():
        return None

    return genai.Client(api_key=str(clave).strip())


def generar_respuesta_gemini(mundo, personaje, mensajes):
    cliente = obtener_cliente_gemini()

    if cliente is None:
        raise ValueError(
            "Falta GEMINI_API_KEY en los Secrets de Streamlit."
        )

    historial = []

    for mensaje in mensajes[-12:]:
        if mensaje.get("role") == "user":
            rol = "Usuario"
        else:
            rol = personaje.get("nombre", "Personaje")

        texto = str(mensaje.get("text", ""))[:3000]
        historial.append(f"{rol}: {texto}")

    prompt = f"""
Actúa como el personaje de una historia interactiva. Responde en español.
Mantén la personalidad, el tono y la continuidad de la historia. No decidas
las acciones ni los pensamientos del usuario. Haz avanzar la escena de forma
natural y deja espacio para que el usuario responda.

UNIVERSO:
Nombre: {mundo.get("nombre", "Mi mundo")}
Descripción: {mundo.get("descripcion", "")}
Género: {mundo.get("genero", "")}
Escena inicial: {mundo.get("escena", "")}
Instrucciones del creador: {mundo.get("instrucciones", "")}

PERSONAJE:
Nombre: {personaje.get("nombre", "Personaje")}
Rol: {personaje.get("rol", "Personaje")}
Personalidad: {personaje.get("personalidad", "Por definir")}

Conversación reciente:
{chr(10).join(historial)}

Continúa como el personaje. Devuelve solo la respuesta del personaje.
"""

    resultado = cliente.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    texto = getattr(resultado, "text", None)

    if not texto or not texto.strip():
        raise RuntimeError("La IA no devolvió una respuesta de texto.")

    return texto.strip()


# ---------- CABECERA Y NAVEGACIÓN ----------
st.markdown("# 🌌 Universe OS")
st.caption("Crea universos. Diseña personajes. Vive historias.")

paginas = [
    ("🏠 Inicio", "Inicio"),
    ("🪐 Mundos", "Mundos"),
    ("✨ Crear", "Crear mundo"),
    ("📖 Historia", "Historia"),
    ("💬 Chats", "Chats"),
    ("⚙️ Apps", "Apps"),
]

columnas = st.columns(6)

for indice, (etiqueta, destino) in enumerate(paginas):
    with columnas[indice]:
        if st.button(
            etiqueta,
            key=f"navegacion_{indice}",
            use_container_width=True
        ):
            st.session_state.pagina = destino
            st.rerun()

st.divider()
pagina = st.session_state.pagina


# ---------- INICIO ----------
if pagina == "Inicio":
    st.markdown("""
    <div class="hero">
      <p>✦ TU ESPACIO CREATIVO</p>
      <h1>¿Qué historia vivirás hoy?</h1>
      <p>Construye mundos, crea personajes y explora nuevas aventuras.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        if st.button("✨ Crear un universo", key="inicio_crear"):
            preparar_creador()

    with b:
        if st.button("🪐 Ver todos mis mundos", key="inicio_mundos"):
            ir_a("Mundos")

    st.markdown("## ✦ Tus universos")

    if not st.session_state.mundos:
        st.info("Aún no tienes mundos. Crea tu primer universo.")

    for mundo in st.session_state.mundos:
        tarjeta_mundo(mundo, "inicio")


# ---------- MUNDOS ----------
elif pagina == "Mundos":
    st.title("🪐 Mis mundos")

    if st.button("＋ Crear un mundo", key="mundos_crear"):
        preparar_creador()

    for mundo in st.session_state.mundos:
        tarjeta_mundo(mundo, "lista")


# ---------- CREADOR POR PASOS ----------
elif pagina == "Crear mundo":
    st.title("✨ Crear un universo")

    nombres_pasos = [
        "Básicos", "Personajes", "Inicio", "Apps", "Instrucciones"
    ]

    paso = st.session_state.paso
    borrador = st.session_state.borrador

    st.progress((paso + 1) / len(nombres_pasos))
    st.caption(f"Paso {paso + 1} de 5 · {nombres_pasos[paso]}")

    if paso == 0:
        st.subheader("🌍 Datos básicos")

        with st.form("form_basicos"):
            nombre = st.text_input(
                "Nombre del mundo",
                value=borrador.get("nombre", "")
            )

            descripcion = st.text_area(
                "Descripción",
                value=borrador.get("descripcion", "")
            )

            opciones_genero = [
                "Anime", "Fantasía", "Aventura", "Drama", "Misterio",
                "Ciencia ficción", "Romance", "Vida cotidiana", "Otro"
            ]

            genero_actual = borrador.get("genero", "Anime")
            indice_genero = (
                opciones_genero.index(genero_actual)
                if genero_actual in opciones_genero else 0
            )

            genero = st.selectbox(
                "Género",
                opciones_genero,
                index=indice_genero
            )

            siguiente = st.form_submit_button("Siguiente →")

        if siguiente:
            if not nombre.strip():
                st.warning("Escribe el nombre de tu mundo.")
            else:
                borrador.update({
                    "nombre": nombre.strip(),
                    "descripcion": descripcion.strip(),
                    "genero": genero
                })
                st.session_state.paso = 1
                st.rerun()

    elif paso == 1:
        st.subheader("🎭 Personajes")

        with st.form("form_personaje", clear_on_submit=True):
            pnombre = st.text_input("Nombre del personaje")
            rol = st.text_input("Rol o relación")
            personalidad = st.text_area("Personalidad y descripción")
            agregar = st.form_submit_button("＋ Añadir personaje")

        if agregar:
            if pnombre.strip():
                st.session_state.personajes_draft.append({
                    "id": str(uuid.uuid4()),
                    "nombre": pnombre.strip(),
                    "rol": rol.strip() or "Personaje",
                    "personalidad": personalidad.strip() or "Por definir"
                })
                st.rerun()
            else:
                st.warning("Escribe un nombre para el personaje.")

        for indice, personaje in enumerate(
            st.session_state.personajes_draft
        ):
            with st.container(border=True):
                st.markdown(
                    f"**{personaje['nombre']}** · {personaje['rol']}"
                )
                st.write(personaje["personalidad"])

                if st.button(
                    "Eliminar personaje",
                    key=f"eliminar_personaje_{personaje['id']}"
                ):
                    st.session_state.personajes_draft.pop(indice)
                    st.rerun()

        anterior, siguiente = st.columns(2)

        with anterior:
            if st.button("← Anterior", key="paso1_atras"):
                st.session_state.paso = 0
                st.rerun()

        with siguiente:
            if st.button("Siguiente →", key="paso1_siguiente"):
                borrador["personajes"] = (
                    st.session_state.personajes_draft[:]
                )
                st.session_state.paso = 2
                st.rerun()

    elif paso == 2:
        st.subheader("📖 Escena inicial")

        with st.form("form_inicio"):
            inicio = st.text_input(
                "Título del comienzo",
                value=borrador.get("inicio", "Un nuevo comienzo")
            )

            escena = st.text_area(
                "¿Qué sucede al comenzar?",
                value=borrador.get("escena", ""),
                height=150
            )

            siguiente = st.form_submit_button("Siguiente →")

        if siguiente:
            borrador["inicio"] = inicio.strip() or "Un nuevo comienzo"
            borrador["escena"] = escena.strip()
            st.session_state.paso = 3
            st.rerun()

        if st.button("← Anterior", key="paso2_atras"):
            st.session_state.paso = 1
            st.rerun()

    elif paso == 3:
        st.subheader("🧩 Aplicaciones del universo")

        opciones_apps = [
            "Historias", "Personajes", "Chats",
            "Diario", "Misiones", "Galería"
        ]

        borrador["apps"] = st.multiselect(
            "Selecciona las aplicaciones",
            opciones_apps,
            default=borrador.get(
                "apps", ["Historias", "Personajes", "Chats"]
            )
        )

        anterior, siguiente = st.columns(2)

        with anterior:
            if st.button("← Anterior", key="paso3_atras"):
                st.session_state.paso = 2
                st.rerun()

        with siguiente:
            if st.button("Siguiente →", key="paso3_siguiente"):
                st.session_state.paso = 4
                st.rerun()

    elif paso == 4:
        st.subheader("📜 Instrucciones")

        instrucciones = st.text_area(
            "Reglas para este universo",
            value=borrador.get("instrucciones", ""),
            height=150,
            placeholder=(
                "Describe el tono, las reglas y cómo deben actuar "
                "los personajes..."
            )
        )

        borrador["instrucciones"] = instrucciones

        st.markdown("### Vista previa")
        st.markdown(f"**{borrador.get('nombre', 'Mi mundo')}**")
        st.write(borrador.get("descripcion", "Sin descripción"))
        st.caption(borrador.get("genero", "Sin género"))
        st.write("Personajes:", len(st.session_state.personajes_draft))
        st.write(
            "Aplicaciones:",
            ", ".join(borrador.get("apps", [])) or "Ninguna"
        )

        anterior, crear = st.columns(2)

        with anterior:
            if st.button("← Anterior", key="paso4_atras"):
                st.session_state.paso = 3
                st.rerun()

        with crear:
            if st.button("🌌 Crear universo", key="guardar_mundo"):
                nombre = borrador.get("nombre", "").strip()

                repetido = any(
                    m.get("nombre", "").casefold() == nombre.casefold()
                    for m in st.session_state.mundos
                )

                if not nombre:
                    st.error("El mundo necesita un nombre.")
                elif repetido:
                    st.error("Ya existe un mundo con ese nombre.")
                else:
                    nuevo = {
                        "id": str(uuid.uuid4()),
                        "nombre": nombre,
                        "descripcion": borrador.get("descripcion", ""),
                        "genero": borrador.get("genero", "Otro"),
                        "personajes": (
                            st.session_state.personajes_draft[:]
                        ),
                        "inicio": borrador.get(
                            "inicio", "Un nuevo comienzo"
                        ),
                        "escena": borrador.get("escena", ""),
                        "instrucciones": instrucciones,
                        "apps": borrador.get("apps", []),
                        "historia": [
                            borrador.get("escena", "").strip()
                            or "Tu aventura acaba de comenzar."
                        ],
                        "chats": {}
                    }

                    st.session_state.mundos.append(nuevo)
                    st.session_state.mundo_id = nuevo["id"]
                    guardar_y_avisar()

                    st.session_state.borrador = {}
                    st.session_state.personajes_draft = []
                    st.session_state.paso = 0
                    ir_a("Historia")


# ---------- HISTORIA ----------
elif pagina == "Historia":
    mundo = obtener_mundo()

    if not mundo:
        st.info("Selecciona un mundo o crea uno nuevo.")

        if st.button("Ir a mundos", key="historia_ir_mundos"):
            ir_a("Mundos")

    else:
        st.title("📖 " + mundo.get("nombre", "Mi mundo"))
        st.caption(mundo.get("genero", "Aventura"))

        if "Historias" not in mundo.get("apps", []):
            st.info("Activa la aplicación Historias en los ajustes del mundo.")
        else:
            for entrada in mundo.get("historia", []):
                with st.container(border=True):
                    st.write(entrada)

            st.markdown("### ¿Qué decides hacer?")

            opciones = [
                "🔎 Explorar el lugar",
                "💬 Hablar con alguien",
                "⚡ Tomar una decisión arriesgada"
            ]

            respuestas = [
                "Encuentras una pista que podría cambiar tu aventura.",
                "Un personaje se acerca y te pregunta qué necesitas.",
                "Tu decisión cambia el rumbo de la historia."
            ]

            columnas_accion = st.columns(3)

            for i, opcion in enumerate(opciones):
                with columnas_accion[i]:
                    if st.button(opcion, key=f"decision_{i}"):
                        mundo.setdefault("historia", []).append(respuestas[i])
                        guardar_y_avisar()
                        st.rerun()

            if st.button("↻ Reiniciar historia", key="reiniciar_historia"):
                mundo["historia"] = [
                    mundo.get("escena", "").strip()
                    or "Tu aventura acaba de comenzar."
                ]
                guardar_y_avisar()
                st.rerun()


# ---------- CHATS CON GEMINI ----------
elif pagina == "Chats":
    st.title("💬 Chats de personajes")
    mundo = obtener_mundo()

    if not mundo:
        st.info("Primero crea o selecciona un mundo.")

    elif "Chats" not in mundo.get("apps", []):
        st.info("Activa la aplicación Chats en los ajustes del mundo.")

    elif not mundo.get("personajes"):
        st.info("Añade personajes al mundo para iniciar conversaciones.")

    else:
        personajes = mundo["personajes"]
        nombres = [p["nombre"] for p in personajes]

        elegido = st.selectbox(
            "Conversar con",
            nombres,
            key=f"personaje_chat_{mundo['id']}"
        )

        personaje = next(
            p for p in personajes if p["nombre"] == elegido
        )

        chats = mundo.setdefault("chats", {})

        mensajes = chats.setdefault(
            elegido,
            [{
                "role": "assistant",
                "text": (
                    f"Hola, soy {elegido}. "
                    "¿Qué te gustaría hacer en esta aventura?"
                )
            }]
        )

        st.caption(personaje.get("rol", "Personaje"))
        st.write(personaje.get("personalidad", ""))

        for mensaje in mensajes:
            rol_visual = mensaje.get("role", "assistant")

            if rol_visual not in ("user", "assistant"):
                rol_visual = "assistant"

            with st.chat_message(rol_visual):

                st.write(mensaje.get("text", ""))

        nuevo_mensaje = st.chat_input(
            f"Escribe a {elegido}...",
            key=f"chat_input_{mundo['id']}_{elegido}"
        )

        if nuevo_mensaje:
            mensajes.append({
                "role": "user",
                "text": nuevo_mensaje
            })

            respuesta = responder_con_gemini(
                mundo=mundo,
                personaje=personaje,
                mensajes=mensajes,
                mensaje_usuario=nuevo_mensaje
            )

            mensajes.append({
                "role": "assistant",
                "text": respuesta
            })

            guardar_y_avisar()
            st.rerun()


# ---------- AJUSTES Y APLICACIONES ----------
elif pagina == "Apps":
    st.title("⚙️ Aplicaciones y ajustes")
    mundo = obtener_mundo()

    if not mundo:
        st.info("Selecciona un mundo primero.")
    else:
        st.markdown("### 🌌 " + mundo.get("nombre", "Mi mundo"))
        st.write(mundo.get("descripcion", ""))

        opciones_apps = [
            "Historias", "Personajes", "Chats",
            "Diario", "Misiones", "Galería"
        ]

        apps = st.multiselect(
            "Aplicaciones instaladas",
            opciones_apps,
            default=mundo.get("apps", []),
            key=f"apps_config_{mundo['id']}"
        )

        instrucciones = st.text_area(
            "Instrucciones del universo",
            value=mundo.get("instrucciones", ""),
            key=f"instrucciones_{mundo['id']}"
        )

        if st.button("💾 Guardar configuración"):
            mundo["apps"] = apps
            mundo["instrucciones"] = instrucciones
            guardar_y_avisar()
            st.success("Configuración actualizada.")

        st.markdown("### 🎭 Personajes")

        for personaje in mundo.get("personajes", []):
            with st.container(border=True):
                st.markdown(
                    f"**{personaje.get('nombre', 'Personaje')}** · "
                    f"{personaje.get('rol', 'Personaje')}"
                )
                st.write(personaje.get("personalidad", ""))


st.divider()
st.caption(
    "UNIVERSE OS · Prototipo en desarrollo. "
    "Los chats usan Gemini cuando la API está configurada."
)

              