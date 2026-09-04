# board/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at') # 어드민 목록에 보여줄 컬럼들
    list_display_links = ('title',) # 제목을 누르면 상세 보기로 이동
    search_fields = ('title', 'content') # 제목과 내용으로 검색