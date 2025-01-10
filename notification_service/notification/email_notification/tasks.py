from celery import shared_task
from .models import Notification
from django.utils.timezone import now
from django.core.mail import send_mail
from .utils import generate_reservation_email_body
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True, queue="reservation_notifications_queue")
def process_notification(self, payload):
    logger.info(f"Received payload: {payload}")
    try:
        notification = Notification.objects.create(
            notif_id=payload.get('reservation_id'),
            member_id=payload.get('member_id'),
            body=f"Reservation for book group {payload.get('book_group_id')}",
            reservation_id=payload.get('reservation_id'),
            is_sent=False
        )

        logger.info(f"Notification created with ID: {notification.notif_id}")

        send_mail(
            subject="Reservation Notification",
            message=generate_reservation_email_body(payload),
            from_email="institution@example.com",
            recipient_list=[payload.get('user_email')],
            fail_silently=False,
        )

        logger.info(f"Email sent to: {payload.get('user_email')}")

        notification.is_sent = True
        notification.sent_datetime = now()
        notification.save()

    except Exception as e:
        logger.error(f"Error in process_notification task: {str(e)}")
