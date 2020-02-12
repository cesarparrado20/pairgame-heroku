web: gunicorn pairgame.wsgi --log-file -
worker: celery -A pairgame worker -l info
beat: celery -A pairgame beat -l info