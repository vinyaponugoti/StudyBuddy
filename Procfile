release: python manage.py migrate
web: gunicorn mysite.wsgi
daphne mysite.asgi:application