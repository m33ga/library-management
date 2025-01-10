from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Reservation, ReservationStatus, UserResponseChoices
from .serializers import ReservationSerializer
from .utils import publish_notification
from itsdangerous import URLSafeTimedSerializer, BadData
from django.utils.timezone import now, timedelta
from django.shortcuts import get_object_or_404
from django.conf import settings
from .utils import generate_action_link
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
import requests

USER_MANAGEMENT_URL = "http://host.docker.internal:8000/decode_token/"

class IsValidToken(BasePermission):
    def has_permission(self, request, view):
        # Extract Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise PermissionDenied({"error": "Authorization token is required"})

        token = auth_header.split(' ')[1]

        # Validate the token
        try:
            response = requests.get(USER_MANAGEMENT_URL, headers={'Authorization': f'Bearer {token}'})
            if response.status_code != 200:
                raise PermissionDenied({"error": "Invalid or expired token"})

            user_data = response.json()
        except requests.RequestException as e:
            raise PermissionDenied({"error": f"Unable to authenticate with user management. Error: {str(e)}"})

        return True

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsValidToken]

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

    def _notify_next_in_queue_logic(self, book_group_id):
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
            return None

        next_reservation.status = ReservationStatus.NOTIFIED
        next_reservation.notification_datetime = now()
        next_reservation.response_deadline = next_reservation.notification_datetime + timedelta(hours=3)
        next_reservation.save()

        accept_link = generate_action_link('accept', next_reservation.id)
        cancel_link = generate_action_link('cancel', next_reservation.id)
        skip_link = generate_action_link('skip', next_reservation.id)


        # member_email = get_member_email(next_reservation.member_id)
        member_email = '123@123.com' # temp
        book_group = 'a book title' # temp

        url = "http://host.docker.internal:8000/get_user/"  # url no bueno
        data = {"user_id": next_reservation.member_id}

        response = requests.post(url, json=data)
        member_email = response.json().get('user', {}).get('email')

        url = "http://host.docker.internal:8081/api/books/title/"  # url no bueno
        data = {"book_group_id": next_reservation.book_group_id}

        response = requests.get(url, json=data)
        book_group = response.json().get('title')
        # DONE: get book group title from book service by ID
        # DONE: get member email from user management service by ID

        publish_notification(
            payload={
                'reservation_id': next_reservation.id,
                'book_group': book_group,
                'user_email': member_email,
                'member_id': next_reservation.member_id,
                'links': {
                    'accept': accept_link,
                    'skip': skip_link,
                    'cancel': cancel_link
                },
            },
            routing_key='reservation.notify'
        )

        # DONE: Implement Celery task for sending notifications to notif service
        # DONE: create cron job for handling non-response in 3 hours
        # DONE: accept reservation and create loan
        # DONE: cancel reservation

        # return data for postman testing
        return {
            "reservation_id": next_reservation.id,
            "links": {
                "accept": accept_link,
                "skip": skip_link,
                "cancel": cancel_link
            }
        }

    @action(detail=False, methods=['post'], url_path='book-group/(?P<book_group_id>[^/.]+)/notify-next')
    def notify_next_in_queue(self, request, book_group_id=None):

        if not book_group_id:
            return Response(
                {"error": "The 'book_group_id' field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = self._notify_next_in_queue_logic(book_group_id)

        if result is None:
            return Response(
                {"message": "No pending reservations found for this book group."},
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": f"User notified for reservation {result['reservation_id']}.",
                "links": result['links'],
            },
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
        reservation = get_object_or_404(Reservation, id=reservation_id)

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

        self._notify_next_in_queue_logic(reservation.book_group_id)

        return Response({"message": "Reservation skipped successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='accept')
    def accept_reservation(self, request):
        token = request.query_params.get('token')
        data = self._validate_token(token)

        if not data:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        reservation_id = data['reservation_id']
        reservation = get_object_or_404(Reservation, id=reservation_id)

        if reservation.status != ReservationStatus.NOTIFIED:
            return Response({"error": "Reservation cannot be accepted in its current state."}, status=status.HTTP_400_BAD_REQUEST)

        reservation.status = ReservationStatus.ACCEPTED
        reservation.user_response = UserResponseChoices.ACCEPT
        reservation.save()

        # TODO: Trigger the loan microservice to create a loan
        # this can and should be done asynchronously with no api call
        response = requests.post(
            'http://host.docker.internal:8083/api/creat_loan_using_book_group_id/',
            json={"member_id": reservation.member_id, "group_book_id": reservation.book_group_id}
        )

        if response.status_code != 201:
            return Response({"error": response.json().get('error')}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Reservation accepted successfully."}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], url_path='cancel')
    def cancel_reservation(self, request):
        token = request.query_params.get('token')
        data = self._validate_token(token)

        if not data:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        reservation_id = data['reservation_id']
        reservation = get_object_or_404(Reservation, id=reservation_id)

        if reservation.status not in [ReservationStatus.NOTIFIED, ReservationStatus.PENDING]:
            return Response({"error": "Reservation cannot be canceled in its current state."}, status=status.HTTP_400_BAD_REQUEST)

        reservation.status = ReservationStatus.CANCELED
        reservation.user_response = UserResponseChoices.CANCEL
        reservation.save()

        self._notify_next_in_queue_logic(reservation.book_group_id)

        return Response({"message": "Reservation canceled successfully."}, status=status.HTTP_200_OK)

