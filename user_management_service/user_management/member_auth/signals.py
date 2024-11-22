from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User

@receiver(post_save, sender=User)
def assign_member_group(sender, instance, created, **kwargs):
    if created:

        group, created = Group.objects.get_or_create(name='member')
        instance.groups.add(group)
