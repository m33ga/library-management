from celery import shared_task
import json
from kombu import Connection, Exchange, Producer
import os
from django.conf import settings
from django.utils.timezone import now
from book_reservations.models import Reservation, ReservationStatus
from  .viewsets import ReservationViewSet
from .utils import publish_notification


@shared_task
def check_expired_reservations():

    expired_reservations = Reservation.objects.filter(
        status=ReservationStatus.NOTIFIED,
        response_deadline__lt=now()
    )

    for reservation in expired_reservations:
        reservation.status = ReservationStatus.EXPIRED
        reservation.save()


        if reservation.book_group_id:
            ReservationViewSet()._notify_next_in_queue_logic(reservation.book_group_id)
