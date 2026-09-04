# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class CustomAuthToken(TokenObtainPairView): # Simple JWT 기본 로그인 뷰 상속
    """ 사용자 정의 로그인 뷰 """
    def post(self, request, *args, **kwargs):
        # 1. ID/PW 검증 및 JWT 토큰 생성 (Simple JWT 본래 기능)
        response = super().post(request, *args, **kwargs) # 로그인 시도 -> ID/PW 검증 -> 토큰 생성 -> 응답 반환 (토큰이 응답 본문에 포함)
        
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            
            # 2. 응답 본문 데이터에서 토큰 내용을 지워, 프론트 앤드의 탈취 위험 방지
            response.data = {'success': True}
            
            # 3. 자바스크립트 접근이 불가능한 HttpOnly 쿠키에 토큰 보관
            response.set_cookie(
                key='accessToken',
                value=access_token,
                httponly=True, # 자바스크립트에서 접근 불가
                secure=not settings.DEBUG,  # True로 설정하면 HTTPS(보안 연결) 환경에서만 쿠키가 전송됨, 개발 환경에서만 False로 동작하도록 설정
                samesite='Lax', # CSRF 공격 방지
                max_age=30 * 60,  # 30분 수명
                path='/' # 사이트 전체 영역에서 이 쿠키를 공유하고 지울 수 있게 설정
            )
            response.set_cookie(
                key='refreshToken',
                value=refresh_token,
                httponly=True, # 자바스크립트에서 접근 불가
                secure=not settings.DEBUG,  # True로 설정하면 HTTPS(보안 연결) 환경에서만 쿠키가 전송됨, 개발 환경에서만 False로 동작하도록 설정
                samesite='Lax', # CSRF 공격 방지
                max_age=7 * 24 * 60 * 60,  # 7일 수명
                path='/' # 사이트 전체 영역에서 이 쿠키를 공유하고 지울 수 있게 설정
            )
            
        return response

class CustomTokenRefreshView(TokenRefreshView):
    """ 사용자 정의 토큰 갱신 뷰 """
    def post(self, request, *args, **kwargs):
        # 1. 쿠키에서 리프레시 토큰 추출
        refresh_token = request.COOKIES.get('refreshToken')
        
        if not refresh_token:
            return Response({"detail": "리프레시 토큰이 쿠키에 없습니다."}, status=400)
            
        # Simple JWT가 인식할 수 있도록 request.data에 주입
        request.data['refresh'] = refresh_token

        try:
            response = super().post(request, *args, **kwargs)
        except (InvalidToken, TokenError) as e:
            # 리프레시 토큰마저 만료되었거나 조작된 경우
            return Response({"detail": f"인증이 만료되었습니다. 다시 로그인해주세요. ({str(e)})"}, status=401)

        # 2. 토큰 갱신 성공 시 새 Access 토큰을 쿠키에 설정
        if response.status_code == 200:
            access_token = response.data['access']
            
            # 응답 본문은 비워서 토큰 탈취 방지
            response.data = {'success': True}
            
            response.set_cookie(
                key='accessToken',
                value=access_token,
                httponly=True, # 자바스크립트에서 접근 불가
                secure=not settings.DEBUG,  # True로 설정하면 HTTPS(보안 연결) 환경에서만 쿠키가 전송됨, 개발 환경에서만 False로 동작하도록 설정
                samesite='Lax', # CSRF 공격 방지
                max_age=30 * 60,  # 30분 수명
                path='/' # 사이트 전체 영역에서 이 쿠키를 공유하고 지울 수 있게 설정
            )
            
        return response
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 로그인한 유저만 로그아웃 요청을 보낼 수 있도록 제한
def logout_view(request):
    # 1. 장고 백엔드 세션이 있다면 서버 측에서 파괴합니다.
    logout(request)
    
    response = JsonResponse({"message": "Successfully logged out."})
    
    # 생성할 때와 똑같은 path='/'로 두 가지 쿠키를 모두 만료시키도록 설정
    cookie_options = {
        'max_age': 0,
        'expires': 0,
        'path': '/',
        'httponly': True,
        'samesite': 'Lax',
        'secure': not settings.DEBUG # True로 설정하면 HTTPS(보안 연결) 환경에서만 쿠키가 전송됨, 개발 환경에서만 False로 동작하도록 설정
    }
    
    # Access Token 삭제 명령
    response.set_cookie('accessToken', '', **cookie_options)
    # Refresh Token도 같이 지워서 새로고침했을 때 자동 갱신 방지
    response.set_cookie('refreshToken', '', **cookie_options)
    
    return response
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 로그인한 사람만 볼 수 있음
def user_info(request):
    """
    현재 로그인한 유저의 정보를 반환하는 View
    """
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "detail": "인증에 성공했습니다."
    })
    
