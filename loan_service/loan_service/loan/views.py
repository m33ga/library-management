from rest_framework import viewsets, status
from .models import Loan, Fine
from .serializers import LoanSerializer, FineSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

USER_MANAGEMENT_URL = "http://host.docker.internal:8000/decode_token/" 


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer

@api_view(['POST'])
def update_returned_date(request):

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
    
    groups = user_data.get('user', {}).get('groups', [])
    is_staff = any(group.get('id') in [2,3] for group in groups)
    if not is_staff:
        raise PermissionDenied({"error": "Access denied. Only staff can perform this action."})
    
    return True

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