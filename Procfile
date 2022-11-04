release: python manage.py migrate
web: daphne mysite.asgi:application --port $PORT -b 0.0.0.0
worker: python manage.py runworker channels --settings=core.settings -v2