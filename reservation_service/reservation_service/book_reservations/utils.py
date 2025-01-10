from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
import uuid
# from celery import shared_task
import json
import pika
# from kombu import Connection, Exchange, Producer


def generate_action_link(action, reservation_id):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps({'action': action, 'reservation_id': reservation_id})
    # test link
    base_url = f"http://localhost/reservation/api/reservations/{action}/"
    return f"{base_url}?token={token}"

RABBITMQ_USER = settings.RABBITMQ_USER
RABBITMQ_PASS = settings.RABBITMQ_PASS
RABBITMQ_HOST = settings.RABBITMQ_HOST
RABBITMQ_PORT = settings.RABBITMQ_PORT
RABBITMQ_VHOST = settings.RABBITMQ_VHOST
RABBITMQ_EXCHANGE = settings.RABBITMQ_EXCHANGE


def publish_notification(payload, routing_key="reservation.notify"):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host=RABBITMQ_VHOST,
        credentials=credentials,
    )

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Declare the exchange if it doesn't already exist
    channel.exchange_declare(
        exchange=RABBITMQ_EXCHANGE,
        exchange_type="direct",
        durable=True,
    )

    # Create the message body
    message_body = json.dumps(payload)

    # Add headers required for Celery to process the task
    message_with_headers = {
        "args": [payload],  # Payload as arguments to the Celery task
        "kwargs": {},  # Empty kwargs, you can add more if needed
    }

    # Publish the message with the required headers
    channel.basic_publish(
        exchange=RABBITMQ_EXCHANGE,
        routing_key=routing_key,
        body=json.dumps(message_with_headers),  # Send the message with the task body
        properties=pika.BasicProperties(
            content_type="application/json",
            headers={
                "id": str(uuid.uuid4()),  # Unique task ID
                "task": "email_notification.tasks.process_notification",  # The Celery task that will process this message
            },
        ),
    )

    connection.close()

    print("Notification published successfully")
