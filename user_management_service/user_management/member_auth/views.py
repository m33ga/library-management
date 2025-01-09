from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from user_management.serializers import UserSerializer, InstitutionSerializer
from member_auth.models import Institution, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.permissions import AllowAny 
from rest_framework_simplejwt.exceptions import InvalidToken

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

class HasAdminPermission(BasePermission):
    def has_permission(self, request, view):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False

        token = auth_header.split(' ')[1]  # Extract token part
        try:
            jwt_authenticator = JWTAuthentication()
            validated_token = jwt_authenticator.get_validated_token(token)  # Validate token
            token_payload = validated_token.payload
            groups = token_payload.get('groups', [])
            return any(group.get('name') == 'admin' for group in groups)

        except InvalidToken as e:
            return False
        except Exception as e:
            return False

# - list_institutions: Returns a list of all institutions.
@api_view(['GET'])
@permission_classes([AllowAny])
def list_institutions(request):
    institutions = Institution.objects.all()
    serializer = InstitutionSerializer(institutions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# - login: Authenticates a user and returns JWT tokens, user data, group info, and institution.
@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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

# - decode_token: Verifies the token and returns user, group, and institution information.
@api_view(['GET'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])      
def decode_token(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    # Retrieve user and institution data from the JWT payload
    user_data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'groups': [{'id': group.id, 'name': group.name} for group in request.user.groups.all()],
    }

    # Retrieve institution info from the JWT token (this is already included in the payload)
    institution_data = {
        'id': request.user.profile.institution.id if request.user.profile.institution else None,
        'name': request.user.profile.institution.name if request.user.profile.institution else None
    }

    # Return user data along with institution info
    return Response({
        'user': user_data,
        'institution': institution_data,
    }, status=status.HTTP_200_OK)

# Admin Views

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, HasAdminPermission])
def create_institution(request):
    serializer = InstitutionSerializer(data=request.data)
    if serializer.is_valid():
        institution = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# - change_user_institution: Allows admins to update the institution for a specific user.
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, HasAdminPermission])
def change_user_institution(request):
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

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, HasAdminPermission])
def change_user_group(request):
    user_id = request.data.get('user_id')
    group_id = request.data.get('group_id')

    if not user_id or not group_id:
        return Response(
            {"error": "'user_id' and 'group_id' must be provided."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if group_id not in [1, 2]:
        return Response(
            {"error": "Only member or staff are allowed."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.user.id == user_id:
        return Response(
            {"error": "You cannot change your own role."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)

        logged_in_user_profile = UserProfile.objects.get(user=request.user)
        target_user_profile = UserProfile.objects.get(user=user)

        if logged_in_user_profile.institution != target_user_profile.institution:
            return Response(
                {"error": "You can only modify the role of users in the same institution."},
                status=status.HTTP_403_FORBIDDEN
            )

        if group in user.groups.all():
            return Response(
                {"message": f"User is already in the {group.name} group."},
                status=status.HTTP_200_OK
            )

        user.groups.clear()
        user.groups.add(group)

        return Response(
            {"message": f"User's group updated successfully to {group.name}."},
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_user(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        return Response({"message": "User found", "user_id": user.id}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)