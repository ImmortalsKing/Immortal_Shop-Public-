import os
from celery import Celery, Task
from kombu import Queue, Exchange
import logging

class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance(exc, ConnectionError):
            logging.error('Connection Error')
        else:
            print(f'task id: {task_id} got error')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KalaMax_Project.settings')
app = Celery('KalaMax_Project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={'x-max-priority': 10}),
    Queue('dead_letter', Exchange('dead_letter'), routing_key='dead_letter'),
]

app.conf.task_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1
app.conf.task_default_queue = 'tasks'
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_routing_key = 'tasks'

app.autodiscover_tasks()