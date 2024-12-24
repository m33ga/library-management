from django.db import models

# Create your models here.
from django.utils.timezone import now

class ReservationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    NOTIFIED = 'notified', 'Notified'
    ACCEPTED = 'accepted', 'Accepted'
    CANCELED = 'canceled', 'Canceled'


class UserResponseChoices(models.TextChoices):
    ACCEPT = 'accept', 'Accept'
    SKIP = 'skip', 'Skip'
    CANCEL = 'cancel', 'Cancel'


class Reservation(models.Model):
    member_id = models.IntegerField()
    book_group_id = models.IntegerField()
    status = models.CharField(
        max_length=10,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,
    )
    reservation_date = models.DateTimeField(default=now)
    notification_datetime = models.DateTimeField(null=True, blank=True)
    response_deadline = models.DateTimeField(null=True, blank=True)
    user_response = models.CharField(
        max_length=10,
        choices=UserResponseChoices.choices,
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.member} reserved {self.book_group}"


