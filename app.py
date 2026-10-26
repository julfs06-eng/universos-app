
import streamlit as st

st.set_page_config(
    page_title="Mundos",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
    max-width: 1100px;
    padding: 2rem 1.2rem 6rem;
}
h1, h2, h3, p {
    color: #f4f6ff;
}
.hero {
    background: linear-gradient(145deg, #1d3260, #11182d);
    border: 1px solid #405bd0;
    border-radius: 24px;
    padding: 26px;
    margin: 18px 0;
}
.world-card {
    background: #111a2e;
    border: 1px solid #283b68;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}
.tag {
    color: #a9bbff;
    font-size: 12px;
    letter-spacing: 1px;
}
.stButton > button {
    background: #536dfe;
    color: white;
    border: 0;
    border-radius: 14px;
    min-height: 44px;
    width: 100%;
    font-weight: 600;
}
.stButton > button:hover {
    background: #7186ff;
    color: white;
    border: 0;
}
[data-testid="stSidebar"] {
    background: #101729;
}
@media (max-width: 600px) {
    .block-container {
        padding: 1rem 0.8rem 5rem;
    }
    .hero {
        padding: 18px;
    }
}
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "Explorar"

if "mundo_activo" not in st.session_state:
    st.session_state.mundo_activo = "My Hero Academia"

st.markdown("# 🌌 Mundos")
st.caption("Historias que puedes vivir")

secciones = ["Explorar", "Chats", "Crear mundo",
             "Comunidad", "Perfil"]

seleccion = st.radio(
    "Navegación",
    secciones,
    horizontal=True,
    label_visibility="collapsed",
    key="nav"
)
st.session_state.pagina = seleccion

if seleccion == "Explorar":
    st.markdown(f"""
    <div class="hero">
      <div class="tag">✦ MUNDO DESTACADO</div>
      <h1>Academia de héroes</h1>
      <p>Tu historia comienza aquí. Tus decisiones
      pueden cambiarlo todo.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶ Continuar historia"):
        st.session_state.pagina = "Chats"
        st.rerun()

    st.markdown("## ✨ Tus mundos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="world-card">
          <div class="tag">DRAMA · AVENTURA</div>
          <h3>🏫 My Hero Academia</h3>
          <p>Una academia, nuevos amigos y
          decisiones que marcarán tu futuro.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Abrir academia"):
            st.session_state.mundo_activo = "My Hero Academia"
            st.session_state.pagina = "Chats"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="world-card">
          <div class="tag">FANTASÍA · MISTERIO</div>
          <h3>🌙 Reinos ocultos</h3>
          <p>Explora un mundo de secretos,
          personajes y aventuras.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Abrir reinos"):
            st.session_state.mundo_activo = "Reinos ocultos"
            st.session_state.pagina = "Chats"
            st.rerun()

elif seleccion == "Chats":
    st.title("💬 Chats")
    st.info(f"Mundo seleccionado: {st.session_state.mundo_activo}")
    st.write("Aquí conectaremos los personajes y las conversaciones.")

elif seleccion == "Crear mundo":
    st.title("✨ Crear un mundo")
    nombre = st.text_input("Nombre del mundo")
    descripcion = st.text_area("Describe su historia")
    genero = st.selectbox(
        "Género",
        ["Fantasía", "Romance", "Drama", "Aventura",
         "Misterio", "Ciencia ficción"]
    )
    if st.button("Crear mundo"):
        if nombre.strip():
            st.success(f"Mundo creado: {nombre} · {genero}")
            st.write(descripcion)
        else:
            st.warning("Escribe un nombre para tu mundo.")

elif seleccion == "Comunidad":
    st.title("👥 Comunidad")
    st.write("Aquí mostraremos mundos publicados y creadores.")

elif seleccion == "Perfil":
    st.title("👤 Mi perfil")
    st.write("Aquí aparecerán tu avatar y tus mundos.")
