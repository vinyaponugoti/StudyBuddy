release: python manage.py migrate
web: daphne mysite.asgi:application
worker: redis-server --port 6390