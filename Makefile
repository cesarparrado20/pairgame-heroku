run:
	./manage.py runserver 0.0.0.0:8002 --settings=pairgame.settings.local
migrate:
	./manage.py makemigrations --settings=pairgame.settings.local
	./manage.py migrate --settings=pairgame.settings.local
superuser:
	./manage.py createsuperuser --settings=pairgame.settings.local
shell:
	./manage.py shell --settings=pairgame.settings.local
clean:
	rm -rf */migrations/00**.py
	find . -name "*.pyc" -exec rm -- {} +
	rm -rf */migrations/__pycache__/*