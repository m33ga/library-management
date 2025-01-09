# reservations/tasks.py
from celery import shared_task
import json
from kombu import Connection, Exchange, Producer
import os
from django.conf import settings

@shared_task
def publish_notification(payload, routing_key):

    # broker_url = os.getenv('CELERY_BROKER_URL')
    # exchange_name = os.getenv('RABBITMQ_EXCHANGE')

    broker_url = settings.CELERY_BROKER_URL
    exchange_name = settings.RABBITMQ_EXCHANGE

    with Connection(broker_url) as connection:
        channel = connection.channel()
        exchange = Exchange(exchange_name, type='topic', durable=True)
        producer = Producer(channel, exchange, serializer='json')

        producer.publish(
            payload,
            routing_key=routing_key,
            retry=True,
            retry_policy={
                'interval_start': 0,
                'interval_step': 2,
                'interval_max': 30,
            }
        )
