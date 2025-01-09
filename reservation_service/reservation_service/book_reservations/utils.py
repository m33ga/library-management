from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def generate_action_link(action, reservation_id):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps({'action': action, 'reservation_id': reservation_id})
    # test link
    base_url = f"http://localhost:8082/api/reservations/{action}/"
    return f"{base_url}?token={token}"
