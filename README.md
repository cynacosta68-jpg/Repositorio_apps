# 🔐 Hub de Aplicaciones — Guía de Instalación

## Estructura del proyecto

```
hub/
├── app.py                  ← App principal del Hub (subir a GitHub)
├── auth.py                 ← Módulo auth para apps hijas (copiar a cada repo)
├── requirements.txt        ← Dependencias
├── secrets_template.toml   ← Template de secrets (NO subir a GitHub)
└── README.md               ← Este archivo
```

---

## Paso 1 — Crear el Hub en GitHub

1. Creá un repo nuevo en GitHub (puede ser público)
2. Subí `app.py` y `requirements.txt`
3. **NO subas** `secrets_template.toml`

---

## Paso 2 — Deployar en Streamlit Cloud

1. Entrá a [share.streamlit.io](https://share.streamlit.io)
2. Conectá el repo del Hub
3. Deployá la app
4. Andá a **Settings → Secrets**
5. Pegá el contenido de `secrets_template.toml` (con tus contraseñas reales)

---

## Paso 3 — Proteger las apps hijas

Para cada app hija, hacé esto:

### 3a. Copiar el módulo auth

Copiá `auth.py` al repo de cada app hija.

### 3b. Editar la URL del Hub

En `auth.py`, cambiá la línea:

```python
HUB_URL = "https://TU-HUB-APP.streamlit.app/"
```

por la URL real de tu Hub desplegado.

### 3c. Agregar el login a cada app

Al inicio de cada `app.py` hija, agregá:

```python
from auth import login_required
login_required()

# --- A partir de acá va tu código normal ---
st.title("Mi App")
```

### 3d. Configurar los secrets en cada app hija

En Streamlit Cloud, para cada app hija, andá a **Settings → Secrets** y pegá:

```toml
[usuarios]
maria = "Clave$egura.2024!"
juan = "0tr@Clave.Fuerte#99"
```

> Los mismos usuarios/contraseñas del Hub, o un subconjunto si querés
> restringir acceso por app.

---

## Paso 4 — Agregar el .gitignore

Asegurate de tener esto en `.gitignore` de cada repo:

```
.streamlit/secrets.toml
```

---

## Flujo del usuario

```
1. Usuario entra al Hub → ve login
2. Se autentica → ve grilla de apps
3. Hace clic en una app → se abre en nueva pestaña
4. La app hija pide login → se autentica de nuevo
5. Usa la app → puede volver al Hub con el botón 🏠
```

---

## Activar roles (futuro)

Cuando necesites que cada usuario vea solo ciertas apps:

1. Descomentá la sección `[roles]` y `[permisos_roles]` en los secrets
2. En `app.py` del Hub, filtrá `APPS` según el rol del usuario logueado
3. En cada app hija, verificá que el usuario tenga permiso

---

## Seguridad

- ✅ Contraseñas en `st.secrets`, nunca en código
- ✅ Comparación con `hmac.compare_digest` (resistente a timing attacks)
- ✅ Repos pueden ser públicos sin exponer credenciales
- ✅ Doble capa de autenticación (Hub + cada app)
- ⚠️ Para datos muy sensibles, considerá hacer los repos privados
- ⚠️ Las contraseñas no están hasheadas (para simplificar); si querés más
  seguridad, usá `streamlit-authenticator` con bcrypt
