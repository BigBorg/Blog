from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)