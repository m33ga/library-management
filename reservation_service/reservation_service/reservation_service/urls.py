from django.contrib import admin
from django.urls import path, include
from book_reservations.routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
