from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from user_management.serializers import UserSerializer, InstitutionSerializer

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    
    if not user.check_password(request.data['password']):
        return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)
    
    token, created = Token.objects.get_or_create(user=user)
    
    groups = user.groups.all()
    group_data = [{'id': group.id, 'name': group.name} for group in groups]

    serializer = UserSerializer(user)
    
    return Response({
        'token': token.key,
        'user': serializer.data,
        'groups': group_data
    })


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        
        groups = user.groups.all()
        group_data = [{'id': group.id, 'name': group.name} for group in groups]

        return Response({
            'token': token.key,
            'user': serializer.data,
            'groups': group_data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):

    serializer = UserSerializer(request.user)
    
    groups = request.user.groups.all()
    group_data = [{'id': group.id, 'name': group.name} for group in groups]
    
    return Response({
        'user': serializer.data,
        'groups': group_data
    }, status=status.HTTP_200_OK)


# TODO DONE MS For now only check if it has a token, after when making the roles check if it has permissions (If it's admin)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
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



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
