# 🎾 Padel Reservas

Sistema completo de gestión de reservas para club de pádel. Desarrollado como proyecto final de Django.

🔗 **URL de producción**: [https://padel-reservas-production.up.railway.app](https://padel-reservas-production.up.railway.app)

---

## 📋 Funcionalidades

### Usuarios (Jugadores)
- **Registro** con nombre de usuario, email, contraseña, nivel de juego y teléfono
- **Perfil editable**: categoría, teléfono, email y foto de perfil
- **Reservas de pistas**: franjas de 30 minutos (09:00–21:00), validación de solapamiento
- **Reservas recurrentes**: misma pista/hora durante 6 meses o 1 año
- **Clases**: inscripción/desinscripción con control de plazas
- **Partidos**: crear, unirse, abandonar, cerrar partido. Opción **mixto**
- **Torneos**: inscripción individual o con pareja (registrada o externa)
- **Pagos**: simulación de pagos automáticos por reservas e inscripciones

### Administrador
- **Crear torneos** desde la interfaz web
- **Gestionar pistas**: activar o poner en mantenimiento
- **Cancelar cualquier reserva**
- **Panel de admin de Django** completo

---

## 🛠️ Tecnologías

| Capa | Tecnología |
|------|------------|
| Backend | Django 4.2 LTS |
| Frontend | Bootstrap 5 + vanilla JS |
| Base de datos | PostgreSQL (producción), SQLite (local) |
| Static files | Whitenoise |
| Deploy | Railway |
| Auth | Django built-in + perfiles extendidos |

---

## 🚀 Cómo ejecutar en local

```bash
# 1. Clonar el repositorio
git clone https://github.com/Baena15/padel-reservas.git
cd padel-reservas

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Ejecutar servidor
python manage.py runserver
```

Abre [http://127.0.0.1:8000](http://127.0.0.1:8000) en tu navegador.

---

## 🔑 Credenciales de prueba (producción)

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Admin | `admin` | `admin123` |

> ⚠️ Cambia la contraseña del admin después de la primera entrega.

---

## 📁 Estructura del proyecto

```
padel-reservas/
├── config/                 # Settings, URLs y WSGI
├── core/                   # Home y vistas base
├── usuarios/               # Auth, registro, perfiles
├── pistas/                 # Pistas y bloqueos
├── reservas/               # Reservas y recurrentes
├── clases/                 # Clases, monitores, inscripciones
├── partidos/               # Partidos y jugadores
├── torneos/                # Torneos e inscripciones
├── pagos/                  # Pagos simulados
├── templates/              # Templates HTML
├── static/                 # CSS/JS estáticos
├── requirements.txt
└── Procfile
```

---

## ⚙️ Variables de entorno (producción)

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta de Django |
| `DATABASE_URL` | PostgreSQL connection string |
| `RAILWAY_PUBLIC_DOMAIN` | Dominio de Railway (auto) |
| `CUSTOM_DOMAIN` | Dominio personalizado (opcional) |
| `DEBUG` | `False` en producción |

---

## 🧑‍💻 Autor

Desarrollado por **Ismael Alfaro Marín** como proyecto final de Django.
