from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment, Like, Follow
from .serializers import PostSerializer, CommentSerializer

class PublicPostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  

class LikePostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, post_id):
        post = generics.get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({"detail": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Liked"}, status=status.HTTP_201_CREATED)

class CommentPostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, post_id):
        post = generics.get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, user_id):
        user_to_follow = generics.get_object_or_404(User, id=user_id)
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        if not created:
            return Response({"detail": "Already following"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Now following"}, status=status.HTTP_201_CREATED)
