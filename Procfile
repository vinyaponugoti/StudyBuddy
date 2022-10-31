release: python manage.py migrate
web: gunicorn mysite.wsgi
web: daphne -b 0.0.0.0 -p $PORT mysite.asgi:application