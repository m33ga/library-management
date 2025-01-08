from rest_framework import serializers
from .models import Loan, Fine
from datetime import timedelta, date
import requests

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

    def create(self, validated_data):
        member_id = validated_data.get('member_id')
        response_member = requests.post(
            'http://host.docker.internal:8000/get_user/',
            json={'user_id': member_id}
        )
        if response_member.status_code != 200:
            raise serializers.ValidationError("Member not found.")
        
        book_copy_id = validated_data.get('book_copy_id')
        response_book = requests.post(
            'http://host.docker.internal:8081/api/reserve_book_copy/',
            json={"book_copy_id": book_copy_id}
        )

        if response_book.status_code != 200:
            raise serializers.ValidationError("Book copy is not available for loan.")

        if 'return_date' not in validated_data or validated_data['return_date'] is None:
            validated_data['return_date'] = date.today() + timedelta(weeks=1)

        validated_data['returned_date'] = None

        return super().create(validated_data)

class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'