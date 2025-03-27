from rest_framework import serializers
from .models import ReservationStatus, UserResponseChoices, Reservation
from django.utils.timezone import now


class ReservationSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField()
    book_group_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=ReservationStatus.choices)
    user_response = serializers.ChoiceField(choices=UserResponseChoices.choices, required=False, allow_null=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'member_id', 'book_group_id', 'status', 'reservation_date',
            'notification_datetime', 'response_deadline', 'user_response'
        ]
        read_only_fields = ['id', 'reservation_date', 'notification_datetime', 'response_deadline']

    def create(self, validated_data):
        validated_data['reservation_date'] = now()
        return super().create(validated_data)
