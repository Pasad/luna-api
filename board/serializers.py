# board/serializers.py
from rest_framework import serializers
from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_id', 'created_at', 'content']