from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

class PublicPostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class LikePostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()
            return Response({"status": "unliked", "likes_count": post.likes.count()}, status=status.HTTP_200_OK)

        return Response({"status": "liked", "likes_count": post.likes.count()}, status=status.HTTP_201_CREATED)

class CommentPostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response({
                "status": "commented",
                "comment": serializer.data,
                "comments_count": post.comments.count()
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
