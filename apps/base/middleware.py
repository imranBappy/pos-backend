
import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from apps.user.models import User  # Adjust the path to your User model

class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get("Authorization", None)
        if token:
            try:
                # Remove "Bearer " from token string
                token = token.split(" ")[1]
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                request.user = User.objects.get(id=payload["user_id"])
            except jwt.ExpiredSignatureError:
                raise Exception("Token expired")
            except jwt.DecodeError:
                raise Exception("Invalid token")
            except User.DoesNotExist:
                raise Exception("User does not exist")
        else:
            request.user = None
