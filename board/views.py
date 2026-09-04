# board/views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  # RetrieveUpdateDestroyAPIView 추가
from rest_framework.pagination import PageNumberPagination  # 페이징 클래스 임포트
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Post
from .serializers import PostListSerializer

# 게시판 표준 페이징 가이드라인 정의
class BoardStandardPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostListSerializer
    
    # 조회(GET)는 누구나(Allow), 생성/수정(POST)은 로그인한 사람만(IsAuthenticated)
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # 리스트 뷰에 방금 만든 페이징 설정을 결합
    pagination_class = BoardStandardPagination

    # 현재 로그인한(인증된) 유저를 작성자로 지정
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    
    # 상세 보기는 누구나(ReadOnly) 가능하지만, 
    # 허가받지 않은 유저가 임의로 PUT/DELETE 공격을 날리는 것을 DRF 단에서 차단
    permission_classes = [IsAuthenticatedOrReadOnly] 
    lookup_field = 'id'