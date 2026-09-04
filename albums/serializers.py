# albums/serializers.py
from rest_framework import serializers
from .models import Album

class AlbumSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source='author.id')
    author_username = serializers.ReadOnlyField(source='author.username')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'author_id', 'author_username', 'image', 'image_url', 'caption', 'location', 'created_at', 'updated_at']
        read_only_fields = ['author_id', 'author_username', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None