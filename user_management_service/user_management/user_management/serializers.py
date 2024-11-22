from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator
from member_auth.models import Institution, UserProfile

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already in use.")]
    )
    password = serializers.CharField(write_only=True, required=True)
    institution_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'institution_id']

    def create(self, validated_data):

        institution_id = validated_data.pop('institution_id')
        user = super().create(validated_data)
        member_group = Group.objects.get(name='member')
        user.groups.add(member_group)
        institution = Institution.objects.get(id=institution_id)
        UserProfile.objects.create(user=user, institution=institution)

        return user


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name']
