# board/serializers.py
from rest_framework import serializers
from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    # 유저ID 대신, username을 가져와 매핑
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'created_at', 'content']