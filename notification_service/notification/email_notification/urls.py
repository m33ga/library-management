from django.urls import path
from .views import NotificationListView, NotificationByMemberView


urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/member/<int:member_id>/', NotificationByMemberView.as_view(), name='notification-by-member'),
]
