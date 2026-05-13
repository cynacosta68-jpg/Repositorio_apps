import streamlit as st
import hmac

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Hub de Aplicaciones",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CATÁLOGO DE APPS (editá acá para agregar/quitar)
# ─────────────────────────────────────────────
APPS = [
    {
        "nombre": "Conversor TXT ISSYS",
        "descripcion": "Conversión de archivos TXT para facturación ISSYS",
        "categoria": "Facturación",
        "subcategoria": "ISSYS",
        "icono": "📄",
        "url": "https://conversor-de-txtissys-6b9famskibdxmvm4tkwcco.streamlit.app/",
    },
    {
        "nombre": "Convertidor Bancario",
        "descripcion": "Conversión de archivos para entidades bancarias",
        "categoria": "Finanzas",
        "subcategoria": "Bancos",
        "icono": "🏦",
        "url": "https://convertidoresbanco-4btwdwlquthvwspn63y8zo.streamlit.app/",
    },
    {
        "nombre": "Templates EVWEB",
        "descripcion": "Generación de templates para facturación EVWEB",
        "categoria": "Facturación",
        "subcategoria": "EVWEB",
        "icono": "📋",
        "url": "https://generacion-de-templates-evweb-eq5xexdbngmzqxhuahwzvn.streamlit.app/",
    },
    {
        "nombre": "INSSJP Internación",
        "descripcion": "Gestión de internación PAMI / INSSJP v2",
        "categoria": "Facturación",
        "subcategoria": "INSSJP",
        "icono": "🏥",
        "url": "https://inssjpinternacionv2-bqwqpnutsegkswun4zynyd.streamlit.app/",
    },
    {
        "nombre": "Proceso de Liquidación",
        "descripcion": "Proceso de liquidación EVWEB",
        "categoria": "Liquidación",
        "subcategoria": "EVWEB",
        "icono": "💰",
        "url": "https://proceso-de-liquidacion-dqf2zqmrmnmxl8utypjmkx.streamlit.app/",
    },
    {
        "nombre": "Valorización SMG",
        "descripcion": "Valorización de prestaciones SMG",
        "categoria": "Facturación",
        "subcategoria": "SMG",
        "icono": "📊",
        "url": "https://valoriacionsmg-gzpmhpc8jyxpzmbtlu6hkh.streamlit.app/",
    },
]

# ─────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Contenedor de login */
    .login-box {
        max-width: 420px;
        margin: 4vh auto 1vh;
        padding: 2rem 2rem 0.5rem;
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 16px;
        background: rgba(128,128,128,0.03);
    }
    .login-box h2 {
        text-align: center;
        margin-bottom: 0.3rem;
        font-size: 1.6rem;
    }
    .login-box p {
        text-align: center;
        color: gray;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* Tarjetas de apps */
    .app-card {
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 12px;
        padding: 1.3rem;
        min-height: 160px;
        transition: all 0.2s ease;
        background: rgba(128,128,128,0.03);
        cursor: pointer;
    }
    .app-card:hover {
        border-color: rgba(59,130,246,0.5);
        box-shadow: 0 4px 12px rgba(59,130,246,0.1);
        transform: translateY(-2px);
    }
    .app-card .icono {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .app-card .nombre {
        font-weight: 600;
        font-size: 1.05rem;
        margin-bottom: 0.3rem;
    }
    .app-card .desc {
        color: gray;
        font-size: 0.85rem;
        margin-bottom: 0.6rem;
    }
    .app-card .badge {
        display: inline-block;
        background: rgba(59,130,246,0.1);
        color: rgba(59,130,246,0.9);
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Header del hub */
    .hub-header {
        text-align: center;
        padding: 1rem 0 0.5rem;
    }
    .hub-header h1 {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
    }
    .hub-header p {
        color: gray;
        font-size: 0.95rem;
    }

    /* Barra superior con usuario */
    .topbar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 0.5rem 0;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid rgba(128,128,128,0.15);
        font-size: 0.85rem;
        color: gray;
    }

    /* Categoría */
    .cat-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1.5rem 0 0.8rem;
        border-left: 3px solid rgba(59,130,246,0.7);
        padding-left: 0.6rem;
    }

    /* Link sin decoración */
    a.app-link {
        text-decoration: none !important;
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AUTENTICACIÓN
# ─────────────────────────────────────────────
def check_password():
    """Verifica credenciales contra st.secrets. Retorna True si ok."""

    def login_clicked():
        username = st.session_state.get("login_user", "")
        password = st.session_state.get("login_pass", "")
        users = st.secrets.get("usuarios", {})

        if username in users and hmac.compare_digest(password, users[username]):
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = username
            del st.session_state["login_pass"]
        else:
            st.session_state["autenticado"] = False
            st.session_state["login_error"] = True

    # Ya autenticado → pasar
    if st.session_state.get("autenticado", False):
        return True

    # Formulario de login
    st.markdown("""
    <div class="login-box">
        <h2>🔐 Hub de Apps</h2>
        <p>Ingresá tus credenciales para continuar</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.text_input("Usuario", key="login_user")
        st.text_input("Contraseña", type="password", key="login_pass")
        st.button("Ingresar", on_click=login_clicked, use_container_width=True, type="primary")

        if st.session_state.get("login_error", False):
            st.error("❌ Usuario o contraseña incorrectos")

    return False


# ─────────────────────────────────────────────
# PANTALLA PRINCIPAL DEL HUB
# ─────────────────────────────────────────────
def mostrar_hub():
    usuario = st.session_state.get("usuario", "")
    nombres = st.secrets.get("nombres", {})
    nombre_completo = nombres.get(usuario, usuario)

    # Barra superior
    col_user, col_logout = st.columns([5, 1])
    with col_user:
        st.markdown(
            f'<div class="topbar">👤 <b>{nombre_completo}</b> &nbsp;·&nbsp; Sesión activa</div>',
            unsafe_allow_html=True,
        )
    with col_logout:
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Header
    st.markdown("""
    <div class="hub-header">
        <h1>📂 Hub de Aplicaciones</h1>
        <p>Seleccioná una aplicación para comenzar</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Filtro por categoría ──
    categorias = sorted(set(app["categoria"] for app in APPS))
    filtro = st.pills("Categoría", ["Todas"] + categorias, default="Todas")

    apps_filtradas = APPS if filtro == "Todas" else [a for a in APPS if a["categoria"] == filtro]

    # ── Agrupar por categoría ──
    cats = {}
    for app in apps_filtradas:
        cats.setdefault(app["categoria"], []).append(app)

    for cat, apps in sorted(cats.items()):
        st.markdown(f'<div class="cat-title">{cat}</div>', unsafe_allow_html=True)

        cols = st.columns(3)
        for i, app in enumerate(apps):
            with cols[i % 3]:
                st.markdown(f"""
                <a href="{app['url']}" target="_blank" class="app-link">
                    <div class="app-card">
                        <div class="icono">{app['icono']}</div>
                        <div class="nombre">{app['nombre']}</div>
                        <div class="desc">{app['descripcion']}</div>
                        <span class="badge">{app['subcategoria']}</span>
                    </div>
                </a>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.caption("🔐 Acceso protegido · Las apps individuales requieren autenticación propia")


# ─────────────────────────────────────────────
# EJECUCIÓN
# ─────────────────────────────────────────────
if not check_password():
    st.stop()

mostrar_hub()
