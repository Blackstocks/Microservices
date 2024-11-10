import json
import requests
from jose import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

class Auth0JSONWebTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        
        token = auth_header.split()[1]
        try:
            # Verifying token
            payload = jwt.decode(
                token,
                requests.get(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json").json(),
                algorithms=["RS256"],
                audience=settings.AUTH0_CLIENT_ID,
                issuer=f"https://{settings.AUTH0_DOMAIN}/"
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("token expired")
        except jwt.JWTClaimsError:
            raise exceptions.AuthenticationFailed("incorrect claims")
        except Exception:
            raise exceptions.AuthenticationFailed("invalid token")
        
        return (payload, None)
