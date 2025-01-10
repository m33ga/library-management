from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Book, Author, Genre, BookCopy
from .serializers import BookSerializer, GenreSerializer, AuthorSerializer, BookCopySerializer
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

USER_MANAGEMENT_URL = "http://host.docker.internal:8000/decode_token/" 

class IsStaffWithValidToken(BasePermission):
    def has_permission(self, request, view):
        # Extract Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise PermissionDenied({"error": "Authorization token is required"})
        
        token = auth_header.split(' ')[1]
        
        # Validate the token
        try:
            response = requests.get(USER_MANAGEMENT_URL, headers={'Authorization': f'Bearer {token}'})
            if response.status_code != 200:
                raise PermissionDenied({"error": "Invalid or expired token"})
            
            user_data = response.json()
        except requests.RequestException as e:
            raise PermissionDenied({"error": f"Unable to authenticate with user management. Error: {str(e)}"})
        
        # Check if the user belongs to the "staff" role (group ID 2)
        groups = user_data.get('user', {}).get('groups', [])
        is_staff = any(group.get('id') in [2,3] for group in groups)
        if not is_staff:
            raise PermissionDenied({"error": "Access denied. Only staff can perform this action."})
        
        # Token and role validation passed
        return True

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffWithValidToken]

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsStaffWithValidToken]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffWithValidToken]

class BookCopyViewSet(viewsets.ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer
    permission_classes = [IsStaffWithValidToken]

@csrf_exempt
@api_view(['POST'])
def books_by_author(request):
    print("Authorization Header:", request.headers.get('Authorization'))
    # Extract the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({"error": "Authorization token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]  # Extract the token part
    
    # Validate the token by calling decode_token in user_management
    try:
        response = requests.get(USER_MANAGEMENT_URL, headers={'Authorization': f'Bearer {token}'})
        if response.status_code != 200:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_data = response.json()  # Extract user data if the token is valid
    except requests.RequestException as e:
        return Response({"error": f"Unable to authenticate with user management. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Proceed with the main functionality
    author_name = request.data.get('author_name')
    if not author_name:
        return Response({"error": "Author name is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        author = Author.objects.get(name__iexact=author_name)
    except Author.DoesNotExist:
        return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
    
    books = Book.objects.filter(author=author)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def books_by_title(request):
    # Extract the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({"error": "Authorization token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]  # Extract the token part
    
    # Validate the token by calling decode_token in user_management
    try:
        response = requests.get(USER_MANAGEMENT_URL, headers={'Authorization': f'Bearer {token}'})
        if response.status_code != 200:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_data = response.json()  # Extract user data if the token is valid
    except requests.RequestException as e:
        return Response({"error": f"Unable to authenticate with user management. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    title = request.data.get('title')
    if not title:
        return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    books = Book.objects.filter(title__iexact=title)
    if not books.exists():
        return Response({"error": "No books found with this title"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def books_by_institution(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({"error": "Authorization token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    
    try:
        response = requests.get(USER_MANAGEMENT_URL, headers={'Authorization': f'Bearer {token}'})
        if response.status_code != 200:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_data = response.json()
    except requests.RequestException as e:
        return Response({"error": f"Unable to authenticate with user management. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    institution_id = request.data.get('institution_id')
    if not institution_id:
        return Response({"error": "Institution ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    books = Book.objects.filter(institution=institution_id)
    if not books.exists():
        return Response({"error": "No books found for this institution"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def reserve_book_copy(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({"error": "Authorization token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    
    try:
        response = requests.get(USER_MANAGEMENT_URL, headers={'Authorization': f'Bearer {token}'})
        if response.status_code != 200:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_data = response.json()
    except requests.RequestException as e:
        return Response({"error": f"Unable to authenticate with user management. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    book_copy_id = request.data.get('book_copy_id')
    if not book_copy_id:
        return Response({"error": "Book copy ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        book_copy = BookCopy.objects.get(id=book_copy_id)
    except BookCopy.DoesNotExist:
        return Response({"error": "Book copy not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if book_copy.status == 'available':
        book_copy.status = 'reserved'
        book_copy.save()
        return Response({"message": "Book copy reserved successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Book copy is already reserved"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def return_book_copy(request):
    # Extract Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({"error": "Authorization token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    
    # Validate token and extract user data
    try:
        response = requests.get(USER_MANAGEMENT_URL, headers={'Authorization': f'Bearer {token}'})
        if response.status_code != 200:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_data = response.json()  # Decode the token data
    except requests.RequestException as e:
        return Response({"error": f"Unable to authenticate with user management. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    # Check if the user belongs to the "staff" role (group ID 2)
    groups = user_data.get('user', {}).get('groups', [])

    is_staff = any(group.get('id') in [2,3] for group in groups)
    if not is_staff:
        return Response({"error": "Access denied. Only staff can perform this action."}, status=status.HTTP_403_FORBIDDEN)
    
    # Process book copy ID
    book_copy_id = request.data.get('book_copy_id')
    if not book_copy_id:
        return Response({"error": "Book copy ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Fetch the book copy
    try:
        book_copy = BookCopy.objects.get(id=book_copy_id)
    except BookCopy.DoesNotExist:
        return Response({"error": "Book copy not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Handle the book copy return logic
    if book_copy.status == 'reserved':
        book_copy.status = 'available'
        book_copy.save()
        return Response({"message": "Book copy returned successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Book copy is already available"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def soft_delete_book_copy(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise PermissionDenied({"error": "Authorization token is required"})

    token = auth_header.split(' ')[1]

    # Validate the token
    try:
        response = requests.get(USER_MANAGEMENT_URL, headers={'Authorization': f'Bearer {token}'})
        if response.status_code != 200:
            raise PermissionDenied({"error": "Invalid or expired token"})

        user_data = response.json()
    except requests.RequestException as e:
        raise PermissionDenied({"error": f"Unable to authenticate with user management. Error: {str(e)}"})

    # Check if the user belongs to the "staff" role (group ID 2 or 3)
    groups = user_data.get('user', {}).get('groups', [])
    is_staff = any(group.get('id') in [2, 3] for group in groups)
    if not is_staff:
        raise PermissionDenied({"error": "Access denied. Only staff can perform this action."})

    # Get user's institution ID from the token response
    user_institution_id = user_data.get('institution', {}).get('id')
    if not user_institution_id:
        raise PermissionDenied({"error": "User's institution could not be determined."})

    # Process book copy ID
    book_copy_id = request.data.get('book_copy_id')
    if not book_copy_id:
        return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the book copy
    try:
        book_copy = BookCopy.objects.select_related('book').get(id=book_copy_id)
    except BookCopy.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the institution of the book matches the user's institution
    if book_copy.book.institution != user_institution_id:
        return Response({"error": "Access denied. The book belongs to a different institution."}, status=status.HTTP_403_FORBIDDEN)

    if book_copy.status == 'reserved' or book_copy.status == 'unavailable':
        return Response({"error": "Book copy is reserved or already unavailable"}, status=status.HTTP_400_BAD_REQUEST)

    # Handle the book copy return logic
    book_copy.deleted = True
    book_copy.status = 'unavailable'
    book_copy.save()

    return Response({"message": "Book soft deleted successfully"}, status=status.HTTP_200_OK)
