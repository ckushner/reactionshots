web: gunicorn shots:app
background: celery -A tasks worker --loglevel=info
flower: celery flower
