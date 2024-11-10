from django.urls import path
from . import views

urlpatterns = [
    path('', views.PublicPostListView.as_view(), name='post_list'),
    path('<int:post_id>/like/', views.LikePostView.as_view(), name='like_post'),
    path('<int:post_id>/comment/', views.CommentPostView.as_view(), name='comment_post'),
]
