release: python manage.py migrate
web: gunicorn esug.wsgi --log-file -
celeryScheduler1: celery -A esug worker -l info
celeryScheduler2: celery -A esug beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler