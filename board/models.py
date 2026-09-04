# board/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    
    # 글 작성자를 장고 기본 유저 모델과 연결
    # 작성자가 탈퇴하더라도 글은 유지되거나 연동되도록 CASCADE를 설정
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="작성자")
    
    # 글이 생성되는 일시를 자동으로 기록하도록 설정
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
        ordering = ['-id']  # 기본 정렬을 최신글 순으로 지정

    def __str__(self):
        return self.title