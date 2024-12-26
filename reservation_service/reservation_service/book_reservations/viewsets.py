from rest_framework import viewsets
from .models import Reservation
from .models import ReservationStatus
from .serializers import ReservationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

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

