
from __future__ import absolute_import, unicode_literals
from celerybeat.celery import app
# from django_celery_results.models import TaskResult


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def xsum2(numbers):
    return sum(numbers)

@app.task
def topic_kompas(numbers):
	from sucker.grab.kompas import visitTopic
	return visitTopic(url,limit)

@app.task
def topic_liputan6(url,limit):
	from sucker.grab.liputan6 import visitTopic
	return visitTopic(url,limit)