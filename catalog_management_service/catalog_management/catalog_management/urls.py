from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet, InstitutionViewSet, GenreViewSet, AuthorViewSet, BookCopyViewSet, books_by_author, books_by_title, books_by_institution

router = DefaultRouter()
router.register(r'book', BookViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'book_copy', BookCopyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/books_by_author/', books_by_author, name='books_by_author'),
    path('api/books_by_title/', books_by_title, name='books_by_title'),
    path('api/books_by_institution/', books_by_institution, name='books_by_institution'),
]