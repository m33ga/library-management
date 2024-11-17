# notification_service/notification/email_notification/serializers.py
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    type = serializers.CharField(default='emails')
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    recipient_list = serializers.ListField(
        child=serializers.EmailField()
    )
