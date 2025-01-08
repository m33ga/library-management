from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from celery import shared_task
import json
from kombu import Connection, Exchange, Producer


def generate_action_link(action, reservation_id):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps({'action': action, 'reservation_id': reservation_id})
    # test link
    base_url = f"http://localhost/reservation/api/reservations/{action}/"
    return f"{base_url}?token={token}"


@shared_task
def publish_notification(payload, routing_key):

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
