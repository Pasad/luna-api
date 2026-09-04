from django.urls import path
from .views import get_jeju_visibility 

urlpatterns = [
    # 함수 이름을 일치시켜 줍니다.
    path('visibility/', get_jeju_visibility, name='visibility'),
]