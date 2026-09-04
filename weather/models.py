from django.db import models

class JejuWeather(models.Model):
    """제주도 주요 지점의 날씨 정보를 저장하는 모델"""
    # 지점명 (예: 표선, 성산)
    name = models.CharField(max_length=50, unique=True)
    
    # 지도 표시를 위한 좌표 (Frontend용)
    lat = models.FloatField(verbose_name="위도")
    lng = models.FloatField(verbose_name="경도")
    
    # 기상청 API 호출을 위한 격자 좌표 (Backend용)
    nx = models.IntegerField(verbose_name="기상청 NX")
    ny = models.IntegerField(verbose_name="기상청 NY")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "제주 지점 정보"
        verbose_name_plural = "제주 지점 정보 목록"