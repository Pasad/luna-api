# weather/views.py
import asyncio
import httpx
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from .models import JejuWeather
from asgiref.sync import sync_to_async  # 장고 ORM의 비동기 조회를 돕는 어댑터

def get_base_datetime():
    """공공데이터는 매시 10분에 최신 정보 오픈, 15분 이전에는 1시간 전 데이터를 조회"""
    now = datetime.now()
    if now.minute < 15:
        target = now - timedelta(hours=1)
    else:
        target = now
    return target.strftime('%Y%m%d'), target.strftime('%H00')

# 개별 지점의 습도를 조회하는 비동기 함수
async def fetch_location_weather(client, loc, base_date, base_time, service_key, api_url):
    params = {
        'serviceKey': service_key,
        'base_date': base_date,
        'base_time': base_time,
        'nx': loc.nx,
        'ny': loc.ny,
        'dataType': 'JSON'
    }
    try:
        # httpx의 비동기 get 요청을 통해 데이터 조회
        response = await client.get(api_url, params=params, timeout=5.0)
        
        if response.status_code == 200:
            # httpx의 .json()은 동기 메서드이므로, 비동기 환경에서는 await 없이 사용 가능
            data = response.json()
            items = data['response']['body']['items']['item']
            obs_data = {item['category']: item['obsrValue'] for item in items}
            
            humidity = f"{obs_data.get('REH', '0')}%"
            temp = f"{obs_data.get('T1H', '0')}°C"
        else:
            humidity, temp = "조회불가", "N/A"
    except Exception as e:
        humidity, temp = "조회불가", "N/A"

    return {
        'name': loc.name,
        'lat': loc.lat,
        'lng': loc.lng,
        'humidity': humidity,
        'temp': temp
    }

# 장고 뷰 함수를 비동기(async def)로 정의
async def get_jeju_visibility(request):
    """제주도 주요 지점의 날씨를 httpx를 활용해 비동기 병렬로 조회하는 뷰"""
    base_date, base_time = get_base_datetime()
    
    # 1. 캐시 확인
    cache_key = f"jeju_weather_{base_date}_{base_time}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return JsonResponse(cached_data, safe=False, json_dumps_params={'ensure_ascii': False})
        
    service_key = settings.DATA_GO_KR_API_KEY
    api_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

    # 2. 장고 ORM 데이터를 비동기로 조회
    get_locations = sync_to_async(lambda: list(JejuWeather.objects.all()))
    target_locations = await get_locations()

    # 3. httpx의 비동기 전용 클라이언트 개방
    async with httpx.AsyncClient() as client:
        # 각 지점별 fetch 작업을 리스트로 매핑 (태스크 예약)
        tasks = [
            fetch_location_weather(client, loc, base_date, base_time, service_key, api_url)
            for loc in target_locations
        ]
        
        # 4. 모든 요청을 한 번에 전송하고, 한 번에 취합 (asyncio.gather를 통해 모든 태스크를 병렬 실행)
        final_results = await asyncio.gather(*tasks)

    # 5. 캐시 저장 및 응답 반환
    cache.set(cache_key, final_results, timeout=1200)

    return JsonResponse(final_results, safe=False, json_dumps_params={'ensure_ascii': False})