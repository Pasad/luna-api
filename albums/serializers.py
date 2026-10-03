# albums/serializers.py
from rest_framework import serializers
from .models import Album

MAX_IMAGE_BYTES = 4 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

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

    def validate_image(self, image):
        if image.size > MAX_IMAGE_BYTES:
            raise serializers.ValidationError("이미지 용량은 4MB 이하여야 합니다.")

        # DRF ImageField는 Pillow로 실제 이미지인지 검증하고, 판별된 형식을 content_type에 담아 줍니다.
        # (확장자나 클라이언트가 보낸 MIME이 아니라 파일 내용 기준)
        if getattr(image, "content_type", None) not in ALLOWED_IMAGE_TYPES:
            raise serializers.ValidationError("JPG, PNG, WEBP, GIF 형식만 업로드할 수 있습니다.")
        return image