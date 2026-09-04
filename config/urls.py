# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')), # 회원 정보 API 관련 URL 추가
    path('api/weather/', include('weather.urls')), # 날씨 API 관련 URL 추가
    path('api/board/', include('board.urls')), # 게시판 API 관련 URL 추가
    path('api/albums/', include('albums.urls')), # 앨범 API 관련 URL 추가
]
