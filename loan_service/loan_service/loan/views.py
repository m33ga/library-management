from rest_framework import viewsets, status
from .models import Loan, Fine
from .serializers import LoanSerializer, FineSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer

@api_view(['POST'])
def update_returned_date(request):
    loan_id = request.data.get('loan_id')
    returned_date = request.data.get('returned_date')
    
    if not loan_id or not returned_date:
        return Response({"error": "Loan ID and returned date are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
    
    loan.returned_date = returned_date
    loan.save()

    book_id = loan.book_copy_id
   
    response = requests.post(
        'http://host.docker.internal:8081/api/return_book_copy/',
        json={"book_copy_id": book_id}
    )

    if response.status_code != 200:
        return Response({"error": "Failed to call the external service"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Returned date updated and external service called successfully"}, status=status.HTTP_200_OK)