from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home_view, auth0_login, auth0_callback, auth0_logout


urlpatterns = [
    path('', home_view, name='home'),  
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('core.apps.users.urls')),
    path('api/posts/', include('core.apps.posts.urls')),
    path('admin/', admin.site.urls),
    path('auth/callback/', auth0_callback, name='auth0_callback'),
    path('auth/login/', auth0_login, name='auth0_login'),  
    path('auth/logout/', auth0_logout, name='auth0_logout'),
    path('api/posts/', include('core.apps.posts.urls')),
]
