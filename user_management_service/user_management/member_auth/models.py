from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.institution.name if self.institution else 'No Institution'}"