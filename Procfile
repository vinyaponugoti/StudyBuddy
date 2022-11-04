release: python manage.py migrate
web: gunicorn mysite.wsgi
daphne -b 0.0.0.0 -p 8001 mysite.asgi:application
redis-server --port 6390