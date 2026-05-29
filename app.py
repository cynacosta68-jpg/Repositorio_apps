import streamlit as st
import hmac

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Hub de Aplicaciones",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CATÁLOGO DE APPS
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
    {
        "nombre": "Foliador de Obras Sociales",
        "descripcion": "Extrae códigos de cuenta de PDFs escaneados y cruza con base de profesionales",
        "categoria": "Facturación",
        "subcategoria": "Obras Sociales",
        "icono": "📑",
        "url": "https://foliadorobras-sociales-vvbbdgu49m7ukd3eow5ep4.streamlit.app/",
    },
    {
        "nombre": "Procesador Galeno",
        "descripcion": "Procesamiento de prestaciones Galeno",
        "categoria": "Facturación",
        "subcategoria": "Galeno",
        "icono": "🏥",
        "url": "https://conexia-seros-backend-production.up.railway.app/",
    },
    {
        "nombre": "Conexia SEROS",
        "descripcion": "Plataforma de gestión Conexia para SEROS",
        "categoria": "Facturación",
        "subcategoria": "SEROS",
        "icono": "🔗",
        "url": "https://conexia-seros-frontend.vercel.app/",
    },
]

# ─────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: linear-gradient(160deg, #060e1a 0%, #0a1628 40%, #0f1f3d 100%);
    }

    /* ── Login ── */
    .login-container {
        max-width: 380px;
        margin: 8vh auto 0;
        text-align: center;
    }
    .login-logo {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    .login-title {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600;
        font-size: 1.5rem;
        color: #e2e8f0;
        margin-bottom: 0.25rem;
    }
    .login-sub {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 300;
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .login-card {
        background: rgba(17, 29, 51, 0.6);
        border: 1px solid rgba(59, 130, 246, 0.08);
        border-radius: 12px;
        padding: 1.75rem;
        backdrop-filter: blur(8px);
    }

    /* ── Inputs ── */
    [data-testid="stTextInput"] input {
        font-family: 'DM Sans', sans-serif !important;
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15) !important;
    }
    [data-testid="stTextInput"] label {
        font-family: 'DM Sans', sans-serif !important;
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        font-weight: 400 !important;
    }

    /* ── Buttons ── */
    .stButton > button, button[kind="primary"] {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.5rem !important;
        letter-spacing: 0.3px;
        transition: all 0.2s ease;
        font-size: 0.85rem !important;
    }
    .stButton > button:hover, button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.25) !important;
    }

    /* ── Topbar ── */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        margin-bottom: 0.25rem;
        border-bottom: 1px solid rgba(59, 130, 246, 0.06);
    }
    .topbar-user {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .topbar-user b { color: #94a3b8; font-weight: 500; }
    .admin-badge {
        background: rgba(59, 130, 246, 0.1);
        color: #60a5fa;
        font-size: 0.65rem;
        font-weight: 500;
        padding: 0.15rem 0.5rem;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }

    /* ── Header ── */
    .hub-header {
        text-align: center;
        padding: 2rem 0 0.5rem;
    }
    .hub-header h1 {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600;
        font-size: 1.8rem;
        color: #e2e8f0;
        letter-spacing: -0.5px;
        margin-bottom: 0.25rem;
    }
    .accent-line {
        width: 40px;
        height: 2px;
        background: #3b82f6;
        margin: 0.6rem auto;
        border-radius: 2px;
    }
    .hub-header p {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 300;
        font-size: 0.9rem;
        color: #64748b;
    }

    /* ── Stats ── */
    .stats-row {
        display: flex;
        gap: 0.75rem;
        margin: 1rem 0 1.5rem;
        justify-content: center;
    }
    .stat-pill {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(59, 130, 246, 0.08);
        border-radius: 8px;
        padding: 0.6rem 1.25rem;
        text-align: center;
    }
    .stat-pill .num {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #60a5fa;
        line-height: 1;
    }
    .stat-pill .lbl {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 0.2rem;
    }

    /* ── Category ── */
    .cat-title {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500;
        font-size: 0.75rem;
        color: #60a5fa;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 1.5rem 0 0.75rem;
        padding-left: 0.1rem;
    }

    /* ── App Cards ── */
    a.app-link {
        text-decoration: none !important;
        color: inherit !important;
        display: block;
    }
    .app-card {
        background: rgba(17, 29, 51, 0.5);
        border: 1px solid rgba(59, 130, 246, 0.06);
        border-radius: 10px;
        padding: 1.2rem;
        min-height: 140px;
        transition: all 0.25s ease;
        cursor: pointer;
        margin-bottom: 0.75rem;
    }
    .app-card:hover {
        border-color: rgba(59, 130, 246, 0.25);
        background: rgba(17, 29, 51, 0.7);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(6, 14, 26, 0.4);
    }
    .app-card .icono {
        font-size: 1.5rem;
        margin-bottom: 0.6rem;
    }
    .app-card .nombre {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        color: #e2e8f0;
        margin-bottom: 0.3rem;
        letter-spacing: -0.2px;
    }
    .app-card .desc {
        font-family: 'DM Sans', sans-serif;
        font-weight: 300;
        color: #64748b;
        font-size: 0.78rem;
        margin-bottom: 0.7rem;
        line-height: 1.4;
    }
    .app-card .badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.08);
        color: #60a5fa;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    .app-card .arrow {
        float: right;
        color: rgba(59, 130, 246, 0.2);
        font-size: 1rem;
        margin-top: -1.8rem;
        transition: color 0.2s;
    }
    .app-card:hover .arrow {
        color: rgba(59, 130, 246, 0.6);
    }

    /* ── Pills filter ── */
    [data-testid="stPills"] button {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.78rem !important;
        border-radius: 20px !important;
    }

    /* ── Alert ── */
    .stAlert { border-radius: 10px !important; }

    /* ── Footer ── */
    .hub-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        border-top: 1px solid rgba(59, 130, 246, 0.04);
        margin-top: 2rem;
    }
    .hub-footer p {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        color: #334155;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AUTENTICACIÓN
# ─────────────────────────────────────────────
def check_password():
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

    if st.session_state.get("autenticado", False):
        return True

    st.markdown("""
    <div class="login-container">
        <div class="login-logo">⚡</div>
        <div class="login-title">Hub de aplicaciones</div>
        <div class="login-sub">Ingresá tus credenciales para continuar</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.text_input("Usuario", key="login_user")
        st.text_input("Contraseña", type="password", key="login_pass")
        st.button("Ingresar", on_click=login_clicked, use_container_width=True, type="primary")
        if st.session_state.get("login_error", False):
            st.error("Usuario o contraseña incorrectos")
        st.markdown('</div>', unsafe_allow_html=True)

    return False


# ─────────────────────────────────────────────
# FILTRO DE APPS POR ROL
# ─────────────────────────────────────────────
def obtener_apps_permitidas(usuario):
    roles = st.secrets.get("roles", {})
    permisos = st.secrets.get("permisos_roles", {})
    rol = roles.get(usuario, "")
    apps_permitidas = permisos.get(rol, [])
    if "*" in apps_permitidas:
        return APPS
    return [app for app in APPS if app["nombre"] in apps_permitidas]


# ─────────────────────────────────────────────
# PANTALLA PRINCIPAL
# ─────────────────────────────────────────────
def mostrar_hub():
    usuario = st.session_state.get("usuario", "")
    nombres = st.secrets.get("nombres", {})
    nombre_completo = nombres.get(usuario, usuario)
    roles = st.secrets.get("roles", {})
    rol = roles.get(usuario, "")
    es_admin = rol == "admin"

    # Topbar
    col_user, col_logout = st.columns([5, 1])
    with col_user:
        admin_html = ' <span class="admin-badge">admin</span>' if es_admin else ''
        st.markdown(
            f'<div class="topbar"><div class="topbar-user">👤 <b>{nombre_completo}</b>{admin_html}</div></div>',
            unsafe_allow_html=True,
        )
    with col_logout:
        if st.button("Cerrar sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Header
    st.markdown("""
    <div class="hub-header">
        <h1>Hub de aplicaciones</h1>
        <div class="accent-line"></div>
        <p>Seleccioná una aplicación para comenzar</p>
    </div>
    """, unsafe_allow_html=True)

    # Apps del usuario
    apps_del_usuario = obtener_apps_permitidas(usuario)

    if not apps_del_usuario:
        st.warning("No tenés apps asignadas. Contactá al administrador.")
        return

    # Stats
    categorias = sorted(set(app["categoria"] for app in apps_del_usuario))
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-pill"><div class="num">{len(apps_del_usuario)}</div><div class="lbl">Apps</div></div>
        <div class="stat-pill"><div class="num">{len(categorias)}</div><div class="lbl">Categorías</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Filtro por categoría
    if len(categorias) > 1:
        filtro = st.pills("Filtrar", ["Todas"] + categorias, default="Todas", label_visibility="collapsed")
        apps_filtradas = apps_del_usuario if filtro == "Todas" else [a for a in apps_del_usuario if a["categoria"] == filtro]
    else:
        apps_filtradas = apps_del_usuario

    # Agrupar por categoría
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
                        <span class="arrow">→</span>
                    </div>
                </a>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div class="hub-footer">
        <p>HUB DE APLICACIONES · {len(apps_del_usuario)} apps disponibles · Acceso protegido</p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# EJECUCIÓN
# ─────────────────────────────────────────────
if not check_password():
    st.stop()

mostrar_hub()
