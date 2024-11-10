from django.urls import path
from .views import PublicPostListView, LikePostView, CommentPostView, FollowUserView

urlpatterns = [
    path('', PublicPostListView.as_view(), name='post_list'),  
    path('<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('<int:post_id>/comment/', CommentPostView.as_view(), name='comment_post'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
]
