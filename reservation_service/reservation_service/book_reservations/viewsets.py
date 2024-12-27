from rest_framework import viewsets
from .models import Reservation
from .models import ReservationStatus, UserResponseChoices
from .serializers import ReservationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now, timedelta
from rest_framework.exceptions import ValidationError
from itsdangerous import URLSafeTimedSerializer, BadData
from django.conf import settings

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


    def perform_create(self, serializer):
        member_id = serializer.validated_data['member_id']
        book_group_id = serializer.validated_data['book_group_id']

        existing_reservation = Reservation.objects.filter(
            member_id=member_id,
            book_group_id=book_group_id,
            status__in=[ReservationStatus.PENDING, ReservationStatus.NOTIFIED]
        ).exists()
        if existing_reservation:
            raise ValidationError(
                {"error": "You already have an active reservation for this book group."}
            )

        active_reservations_count = Reservation.objects.filter(
            member_id=member_id,
            status__in=[ReservationStatus.PENDING, ReservationStatus.NOTIFIED]
        ).count()

        if active_reservations_count >= 10:
            raise ValidationError(
                {"error": "You cannot have more than 10 active reservations."}
            )

        serializer.save(reservation_date=now())


    @action(detail=False, methods=['get'], url_path='book-group/(?P<book_group_id>[^/.]+)/active')
    def active_queue(self, request,  book_group_id=None):
        if not book_group_id:
            return Response(
                {"error": "The 'book_group_id' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book_group_id = int(book_group_id)
        except ValueError:
            return Response(
                {"error": "The 'book_group_id' query parameter must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        active_reservations = self.queryset.filter(
            status__in=[ReservationStatus.PENDING, ReservationStatus.NOTIFIED],
            book_group_id=book_group_id
        )

        if not active_reservations.exists():
            return Response(
                {"message": "No active reservations found for the specified book group."},
                status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(active_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='book-group/(?P<book_group_id>[^/.]+)/next')
    def next_in_queue(self, request, book_group_id=None):

        if not book_group_id:
            return Response(
                {"error": "The 'book_group_id' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book_group_id = int(book_group_id)
        except ValueError:
            return Response(
                {"error": "The 'book_group_id' query parameter must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        filters = {'status': ReservationStatus.PENDING}
        if book_group_id is not None:
            filters['book_group_id'] = book_group_id

        next_reservation = self.queryset.filter(**filters).order_by('reservation_date').first()

        if not next_reservation:
            return Response(
                {"message": "No pending reservations found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(next_reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='book-group/(?P<book_group_id>[^/.]+)/count')
    def queue_length(self, request, book_group_id=None):

        if not book_group_id:
            return Response(
                {"error": "The 'book_group_id' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book_group_id = int(book_group_id)
        except ValueError:
            return Response(
                {"error": "The 'book_group_id' query parameter must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        filters = {'status': ReservationStatus.PENDING}
        if book_group_id is not None:
            filters['book_group_id'] = book_group_id

        queue_length = self.queryset.filter(**filters).count()

        response_data = {'queue_length': queue_length}
        if book_group_id:
            response_data['book_group_id'] = book_group_id

        return Response(response_data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='member/(?P<member_id>[^/.]+)/active')
    def active_reservations_for_member(self, request, member_id=None):

        if not member_id:
            return Response(
                {"error": "The 'member_id' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            member_id = int(member_id)
        except ValueError:
            return Response(
                {"error": "The 'member_id' query parameter must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        filters = {'status': ReservationStatus.PENDING}
        if member_id is not None:
            filters['member_id'] = member_id

        member_reservations = self.queryset.filter(**filters)
        if not member_reservations.exists():
            return Response(
                {"message": f"No reservations found for member_id: {member_id}."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(member_reservations, many=True)
        return Response(
            {
                "member_id": member_id,
                "reservations": serializer.data
            },
            status=status.HTTP_200_OK
        )


    @action(detail=False, methods=['get'], url_path='member/(?P<member_id>[^/.]+)/all')
    def all_reservations_for_member(self, request, member_id=None):

        if not member_id:
            return Response(
                {"error": "The 'member_id' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            member_id = int(member_id)
        except ValueError:
            return Response(
                {"error": "The 'member_id' query parameter must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        member_reservations = self.queryset.filter(member_id=member_id)
        if not member_reservations.exists():
            return Response(
                {"message": f"No reservations found for member_id: {member_id}."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(member_reservations, many=True)
        return Response(
            {
                "member_id": member_id,
                "reservations": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='book-group/(?P<book_group_id>[^/.]+)/all')
    def reservations_for_book_group(self, request, book_group_id=None):

        if not book_group_id:
            return Response(
                {"error": "The 'book_group_id' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book_group_id = int(book_group_id)
        except ValueError:
            return Response(
                {"error": "The 'book_group_id' query parameter must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        book_group_reservations = self.queryset.filter(book_group_id=book_group_id)
        if not book_group_reservations.exists():
            return Response(
                {"message": f"No reservations found for book_group_id: {book_group_id}."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(book_group_reservations, many=True)
        return Response(
            {
                "book_group_id": book_group_id,
                "reservations": serializer.data
            },
            status=status.HTTP_200_OK
        )


    @action(detail=False, methods=['post'], url_path='book-group/(?P<book_group_id>[^/.]+)/notify-next')
    def notify_next_in_queue(self, request, book_group_id=None):

        if not book_group_id:
            return Response(
                {"error": "The 'book_group_id' field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        next_reservation = (
            self.queryset
            .filter(
                book_group_id=book_group_id,
                status=ReservationStatus.PENDING
            )
            .order_by('reservation_date')
            .first()
        )

        if not next_reservation:
            return Response(
                {"message": "No pending reservations found for this book group."},
                status=status.HTTP_200_OK
            )

        next_reservation.status = ReservationStatus.NOTIFIED
        next_reservation.notification_datetime = now()
        next_reservation.response_deadline = next_reservation.notification_datetime + timedelta(hours=3)
        next_reservation.save()

        # TODO: Implement Celery task for sending notifications to notif service
        # TODO: create cron job for handling non-response in 3 hours
        # TODO: accept reservation and create loan
        # TODO: cancel reservation

        # send_notification.delay(next_reservation.id)

        return Response(
            {"message": f"User notified for reservation {next_reservation.id}."},
            status=status.HTTP_200_OK
        )


    def _validate_token(self, token):
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        try:
            data = serializer.loads(token, max_age=10800)  # Token valid for 3 hours
            return data
        except BadData:
            return None


    @action(detail=False, methods=['post'], url_path='skip')
    def skip_reservation(self, request):
        token = request.query_params.get('token')
        data = self._validate_token(token)

        if not data:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        reservation_id = data['reservation_id']
        reservation = self.get_object_or_404(Reservation, id=reservation_id)

        if reservation.status != ReservationStatus.NOTIFIED:
            return Response({"error": "Reservation cannot be skipped in its current state."}, status=status.HTTP_400_BAD_REQUEST)

        reservation.status = ReservationStatus.CANCELED
        reservation.user_response = UserResponseChoices.SKIP
        reservation.save()

        Reservation.objects.create(
            member_id=reservation.member_id,
            book_group_id=reservation.book_group_id,
            status=ReservationStatus.PENDING,
            reservation_date=now()
        )

        # TODO: trigger notify next in queue
        # here

        return Response({"message": "Reservation skipped successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='accept')
    def accept_reservation(self, request):
        token = request.query_params.get('token')
        data = self._validate_token(token)

        if not data:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        reservation_id = data['reservation_id']
        reservation = self.get_object_or_404(Reservation, id=reservation_id)

        if reservation.status != ReservationStatus.NOTIFIED:
            return Response({"error": "Reservation cannot be accepted in its current state."}, status=status.HTTP_400_BAD_REQUEST)

        reservation.status = ReservationStatus.ACCEPTED
        reservation.user_response = UserResponseChoices.ACCEPT
        reservation.save()

        # TODO: Trigger the loan microservice to create a loan
        # here

        return Response({"message": "Reservation accepted successfully."}, status=status.HTTP_200_OK)

