from django.contrib import admin
from django.urls import path, include
from loan.views import LoanViewSet, FineViewSet, update_returned_date, creat_loan_using_book_group_id
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'loan', LoanViewSet)
router.register(r'fine', FineViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/update_returned_date/', update_returned_date, name='update_returned_date'),
    path('api/creat_loan_using_book_group_id/', creat_loan_using_book_group_id, name='creat_loan_using_book_group_id'),
]
