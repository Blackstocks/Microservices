from rest_framework import serializers
from .models import Post, Comment, Like, Follow

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'created_at', 'comments', 'likes']
