from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from user_management.serializers import UserSerializer, InstitutionSerializer
from member_auth.models import Institution
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# Helper function to generate JWT tokens
def get_tokens_for_user(user):
    # Create refresh token
    refresh = RefreshToken.for_user(user)

    # Adding custom claims to the tokens
    refresh.payload['username'] = user.username
    refresh.payload['email'] = user.email
    refresh.payload['groups'] = [{'id': group.id, 'name': group.name} for group in user.groups.all()]
    
    # Including institution data
    profile = user.profile
    institution_data = {
        "id": profile.institution.id if profile.institution else None,
        "name": profile.institution.name if profile.institution else None
    }
    refresh.payload['institution'] = institution_data

    # Access token carries the same information
    access_token = refresh.access_token
    access_token.payload['username'] = user.username
    access_token.payload['email'] = user.email
    access_token.payload['groups'] = [{'id': group.id, 'name': group.name} for group in user.groups.all()]
    access_token.payload['institution'] = institution_data

    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }

# - list_institutions: Returns a list of all institutions.
@api_view(['GET'])
def list_institutions(request):
    institutions = Institution.objects.all()
    serializer = InstitutionSerializer(institutions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# - login: Authenticates a user and returns JWT tokens, user data, group info, and institution.
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])

    if not user.check_password(request.data['password']):
        return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)

    tokens = get_tokens_for_user(user)

    return Response({
        'tokens': tokens
    })

# - signup: Registers a new user, creates their profile, assigns institution info, and returns JWT tokens, user data, group info, and institution.
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()

        tokens = get_tokens_for_user(user)

        return Response({
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Basic Member Views

# - test_token: Verifies the token and returns user, group, and institution information.
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    # The `request.user` will be populated with the user info from the token
    serializer = UserSerializer(request.user)

    # Get user groups from the token
    groups = request.user.groups.all()
    group_data = [{'id': group.id, 'name': group.name} for group in groups]

    # Accessing the custom claims like institution
    institution_data = request.user.profile.institution if hasattr(request.user, 'profile') else None

    return Response({
        'user': serializer.data,
        'groups': group_data,
        'institution': institution_data
    }, status=status.HTTP_200_OK)

# Admin Views

# - create_institution: Allows admins to create a new institution.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_institution(request):
    # The ID 3 is the admin role
    if not request.user.groups.filter(id=3).exists():
        return Response(
            {"error": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = InstitutionSerializer(data=request.data)
    if serializer.is_valid():
        institution = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# - change_user_institution: Allows admins to update the institution for a specific user.
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_user_institution(request):
    if not request.user.groups.filter(id=3).exists():
        return Response(
            {"error": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )

    user_id = request.data.get('user_id')
    new_institution_id = request.data.get('institution_id')

    if not user_id or not new_institution_id:
        return Response(
            {"error": "Both 'user_id' and 'institution_id' must be provided."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=user_id)
        institution = Institution.objects.get(id=new_institution_id)

        profile = user.profile
        profile.institution = institution
        profile.save()

        return Response(
            {
                "message": "User's institution updated successfully.",
                "user_id": user.id,
                "new_institution": {"id": institution.id, "name": institution.name}
            },
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
