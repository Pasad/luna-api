# accounts/authenticate.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    프론트엔드가 HttpOnly 쿠키로 보낸 accessToken을 꺼내서 유저 인증을 처리하는 클래스
    """
    def authenticate(self, request):
        # 쿠키에서 'accessToken' 조회
        raw_token = request.COOKIES.get('accessToken')
        
        if raw_token is None:
            return None

        # 꺼낸 토큰을 Simple JWT의 검증 로직으로 유저 식별
        validated_token = self.get_validated_token(raw_token)

        # CSRF 검증 면제 설정
        request._dont_enforce_csrf_for_this_request = True
        
        return self.get_user(validated_token), validated_token

