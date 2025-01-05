from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet, InstitutionViewSet, GenreViewSet, AuthorViewSet, BookCopyViewSet

router = DefaultRouter()
router.register(r'book', BookViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'book_copy', BookCopyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Inclui as rotas geradas pelo roteador
]