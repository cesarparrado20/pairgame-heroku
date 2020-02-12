web: gunicorn pairgame.wsgi --log-file -
worker: celery -A pairgame worker -l info
beat: celery -A api_pairgame beat -l info