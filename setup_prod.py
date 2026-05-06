import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@padel.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')

from pistas.models import Pista
if Pista.objects.count() == 0:
    for i in range(1, 9):
        Pista.objects.create(nombre=f'Pista Indoor {i}', tipo='indoor')
    for i in range(1, 7):
        Pista.objects.create(nombre=f'Pista Outdoor {i}', tipo='outdoor')
    print('14 courts created')
else:
    print('Courts already exist')
