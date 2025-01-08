from rest_framework import serializers
from .models import Loan, Fine
from datetime import timedelta, datetime

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

    # def create(self, validated_data):
    #     if 'loan_date' not in validated_data or validated_data['loan_date'] is None:
    #         validated_data['loan_date'] = datetime.now()
    #     if 'return_date' not in validated_data or validated_data['return_date'] is None:
    #         validated_data['return_date'] = validated_data['loan_date'] + timedelta(weeks=1)
    #     return super().create(validated_data)

class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'