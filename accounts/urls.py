# accounts/urls.py
from django.urls import path
from .views import CustomAuthToken, CustomTokenRefreshView, user_info, logout_view

urlpatterns = [
    # 로그인 API
    path('login/', CustomAuthToken.as_view(), name='token_obtain_pair'),
    # 토큰 갱신
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),    
    # 로그아웃 API
    path('logout/', logout_view, name='logout'),    
    # 유저 정보 조회 API
    path('user-info/', user_info, name='user_info'),
]