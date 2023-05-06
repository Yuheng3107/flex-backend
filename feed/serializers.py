from rest_framework import serializers
from .models import Comment, FeedPost

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['likers']

class FeedPostSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = FeedPost
        exclude = ['likers']