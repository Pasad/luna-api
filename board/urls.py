# board/urls.py
from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveAPIView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:id>/', PostRetrieveAPIView.as_view(), name='post-detail'),
]