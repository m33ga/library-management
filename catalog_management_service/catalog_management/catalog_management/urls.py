from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet, InstitutionViewSet, GenreViewSet, BookAuthorViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'do', GenreViewSet)
router.register(r'book-authors', BookAuthorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Inclui as rotas geradas pelo roteador
]