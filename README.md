# Padel Reservas

Aplicación de reservas de pistas de pádel con sistema de clases, partidos y torneos.

## Stack
- Django 4.2 LTS
- Bootstrap 5
- PostgreSQL (producción) / SQLite (desarrollo)
- Whitenoise + Gunicorn

## Instalación local
```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Superusuario
- Usuario: `admin`
- Contraseña: `admin123`

## Features implementadas
- ✅ 14 pistas (8 indoor + 6 outdoor)
- ✅ Sistema de reservas con validaciones (90min, 9-21h, sin solapamiento)
- ✅ Reservas recurrentes (6 meses / 1 año)
- ✅ Auth (login/registro/perfil)
- ⏳ Clases con monitores
- ⏳ Matchmaking de partidos
- ⏳ Torneos
- ⏳ Pagos simulados

## Deploy
Configurado para Railway con variables de entorno en `.env`.
