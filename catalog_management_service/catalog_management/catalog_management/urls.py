from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet, GenreViewSet, AuthorViewSet, BookCopyViewSet, books_by_author, books_by_title, books_by_institution, reserve_book_copy, return_book_copy, soft_delete_book_copy, verify_book_copy_availability_in_bookgroup

router = DefaultRouter()
router.register(r'book', BookViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'book_copy', BookCopyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/books_by_author/', books_by_author, name='books_by_author'),
    path('api/books_by_title/', books_by_title, name='books_by_title'),
    path('api/books_by_institution/', books_by_institution, name='books_by_institution'),
    path('api/reserve_book_copy/', reserve_book_copy, name='reserve_book_copy'),
    path('api/return_book_copy/', return_book_copy, name='return_book_copy'),
    path('api/soft_delete_book_copy/', soft_delete_book_copy, name='soft_delete_book_copy'),
    path('api/verify_book_copy_availability_in_bookgroup/', verify_book_copy_availability_in_bookgroup, name='verify_book_copy_availability_in_bookgroup'),
]