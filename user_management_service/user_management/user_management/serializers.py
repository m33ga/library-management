from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Institution

class UserSerializer (serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields =  ['id', 'username', 'password', 'email']

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name']
