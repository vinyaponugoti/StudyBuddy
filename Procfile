release: python manage.py migrate
web: gunicorn mysite.wsgi
daphne -p 8001 mysite.asgi:application