from django.db import models

# Create your models here.
from django.utils.timezone import now

class Notification(models.Model):
    notif_id = models.CharField(max_length=255, unique=True)
    member_id = models.IntegerField()
    body = models.TextField()
    sent_datetime = models.DateTimeField(default=now)
    reservation_id = models.IntegerField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.notif_id} to Member {self.member_id}"
