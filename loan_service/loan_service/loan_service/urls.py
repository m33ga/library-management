from django.contrib import admin
from django.urls import path, include
from loan.views import LoanViewSet, FineViewSet, update_returned_date
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'loan', LoanViewSet)
router.register(r'fine', FineViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/update_returned_date/', update_returned_date, name='update_returned_date'),
]
