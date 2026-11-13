# Comal - sitio de cocina y API de usuarios

Comal combina una página de recetas con una API Django REST Framework. El proyecto implementa usuarios con inicio de sesión por correo, teléfono como campo adicional, CRUD protegido, datos personales y autenticación JWT documentada con Swagger.

## Requisitos

- Python 3.10 o posterior
- pip

## Instalación local en Windows

Desde esta carpeta, abre PowerShell y ejecuta:

~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
~~~

Abre la página en http://127.0.0.1:8000/ y Swagger en http://127.0.0.1:8000/api/docs/. El admin está en http://127.0.0.1:8000/admin/.

## Endpoints principales

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET, POST | /api/usuarios/ | Listado (solo staff) y registro |
| GET, PUT, PATCH, DELETE | /api/usuarios/{id}/ | CRUD del propio usuario; staff puede gestionar todos |
| GET | /api/datos-personales/ | Datos del usuario autenticado con JWT |
| POST | /api/token/ | Obtiene access y refresh token con correo y contraseña |
| POST | /api/token/refresh/ | Renueva el access token |
| GET | /api/docs/ | Interfaz Swagger |
| GET | /api/schema/ | Esquema OpenAPI |

## Seguridad aplicada

- password es write_only en el serializer; las respuestas del CRUD no devuelven contraseña ni hash.
- El endpoint de datos personales usa un serializer de lectura explícito que no incluye contraseña.
- En actualización, solo se llama a set_password si se envió una contraseña nueva; omitirla conserva el hash actual.
- Las personas usuarias solo pueden consultar o cambiar su propio registro. La lista completa queda reservada para staff.
- ACCESS_TOKEN_LIFETIME está configurado en 15 minutos.
- phone aparece en admin, serializer y Swagger.

## Evidencias para el PDF

1. Arranca el servidor y toma una captura de /api/docs/ donde se vean los endpoints y el título **Comal | API de cocina**.
2. En Swagger, usa POST /api/token/ con email y password. Captura la respuesta con access y refresh token. Evita compartir el token fuera de la evidencia de clase.
3. Copia el access token en Authorize como Bearer <token>; ejecuta GET /api/datos-personales/ y captura la respuesta. Debe aparecer phone y no debe aparecer password.
4. Para demostrar que editar sin contraseña no cambia la contraseña, usa un usuario de práctica:
   - Inicia sesión y captura el access token.
   - Ejecuta PATCH /api/usuarios/{id}/ enviando solo, por ejemplo, {"phone":"555-0101"}.
   - Cierra sesión en Swagger y vuelve a iniciar sesión con la contraseña original en POST /api/token/.
   - Captura el cambio de teléfono y el inicio de sesión exitoso con la contraseña original.

Inserta esas capturas en un documento con el enlace al repositorio de GitHub y expórtalo a PDF. Las capturas deben salir de la ejecución real del proyecto.

## GitHub

Antes de subir, comprueba que .gitignore excluye .venv/ y db.sqlite3. No subas secretos ni bases de datos locales. La clave de settings.py es solo para desarrollo local y debe reemplazarse por una variable de entorno antes de desplegar.
