from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Book, Author, Institution, Genre, BookCopy
from .serializers import BookSerializer, InstitutionSerializer, GenreSerializer, AuthorSerializer, BookCopySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookCopyViewSet(viewsets.ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer

@api_view(['POST'])
def books_by_author(request):
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

@api_view(['POST'])
def books_by_title(request):
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
    institution_name = request.data.get('institution_name')
    if not institution_name:
        return Response({"error": "Institution name is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        institution = Institution.objects.get(name__iexact=institution_name)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)
    
    books = Book.objects.filter(institution=institution)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def reserve_book_copy(request):
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
    book_copy_id = request.data.get('book_copy_id')
    if not book_copy_id:
        return Response({"error": "Book copy ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        book_copy = BookCopy.objects.get(id=book_copy_id)
    except BookCopy.DoesNotExist:
        return Response({"error": "Book copy not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if book_copy.status == 'reserved':
        book_copy.status = 'available'
        book_copy.save()
        return Response({"message": "Book copy returned successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Book copy is already available"}, status=status.HTTP_400_BAD_REQUEST)