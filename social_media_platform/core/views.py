import json
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from jose import jwt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, JsonResponse

def auth0_login(request):
    auth_url = (
        f"https://{settings.AUTH0_DOMAIN}/authorize?"
        f"client_id={settings.AUTH0_CLIENT_ID}&"
        f"redirect_uri={request.build_absolute_uri(reverse('auth0_callback'))}&"
        f"response_type=code&"
        f"scope=openid profile email"
    )
    return HttpResponseRedirect(auth_url)


def auth0_callback(request):
    code = request.GET.get("code")
    token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    token_payload = {
        "grant_type": "authorization_code",
        "client_id": settings.AUTH0_CLIENT_ID,
        "client_secret": settings.AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": request.build_absolute_uri(reverse('auth0_callback')),
    }

    token_response = requests.post(token_url, json=token_payload)
    tokens = token_response.json()
    id_token = tokens.get("id_token")

    if id_token:
        user_info = jwt.decode(
            id_token,
            requests.get(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json").json(),
            algorithms=["RS256"],
            audience=settings.AUTH0_CLIENT_ID,
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )

        user, created = User.objects.get_or_create(username=user_info["sub"])
        user.first_name = user_info.get("given_name", "")
        user.last_name = user_info.get("family_name", "")
        user.email = user_info.get("email", "")
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        response = HttpResponseRedirect('/')
        response.set_cookie('isAuthenticated', 'true')
        return response

    return JsonResponse({"error": "Authentication failed"}, status=400)


def auth0_logout(request):
    logout(request)
    auth0_logout_url = (
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        f"client_id={settings.AUTH0_CLIENT_ID}&"
        f"returnTo={request.build_absolute_uri('/')}"
    )
    response = HttpResponseRedirect(auth0_logout_url)
    response.delete_cookie('isAuthenticated')  
    return response


def home_view(request):
    return render(request, "facebook_ui.html")
