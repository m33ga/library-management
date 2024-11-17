# notification_service/notification/email_notification/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import EmailSerializer

class SendEmailView(APIView):
    """
    API endpoint to send an email.
    """
    resource_name = 'emails'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to send an email.
        
        Expects a JSON payload with the following structure:
        {
           "data": {
                "type": "emails",
                "attributes": {
                    "subject": "Test Subject",
                    "message": "This is a test message.",
                    "recipient_list": ["recipient@example.com"]
                }
            }
        }
        
        Returns a 200 OK response if the email is sent successfully,
        or a 400 Bad Request response if the input data is invalid.
        """
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            recipient_list = serializer.validated_data['recipient_list']
            send_mail(subject, message, 'your_email@example.com', recipient_list)
            return Response({'status': 'Email sent'}, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)