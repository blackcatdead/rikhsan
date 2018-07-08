# rikhsan
damnproject

celery -A celerybeat beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

celery -A celerybeat worker -l info
celery -A celerybeat worker -l info


service celeryd start
service celerybeat start


service celerybeat stop
service celeryd stop

service mysqld status

ssh root@167.99.65.216

