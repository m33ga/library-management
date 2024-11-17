from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator
from member_auth.models import Institution

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already in use.")]
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        user = super().create(validated_data)

        member_group = Group.objects.get(name='member')
        user.groups.add(member_group)
        return user

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name']
