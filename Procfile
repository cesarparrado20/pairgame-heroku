web: gunicorn pairgame.wsgi --log-file -
worker: celery -A pairgame worker -B -l info