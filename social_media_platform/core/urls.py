from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint to get JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint to refresh JWT
    path('api/users/', include('core.apps.users.urls')),  # Users API 
    path('api/posts/', include('core.apps.posts.urls')),  # Posts API 
    path('api/social/', include('core.apps.social.urls')),  # Social API 
    path('api/notifications/', include('core.apps.notifications.urls')),  # Notifications API 
]
