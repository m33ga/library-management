from rest_framework.routers import DefaultRouter
from .viewsets import ReservationViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet)
