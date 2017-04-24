from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.filters import OrderingFilter
from .paginations import PostLimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
)
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer
)
from posts.models import Post
from .permissions import IsOwnerOrReadOnly

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
    # for reference
    # lookup_url_kwarg = "abc"

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "slug"

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = "slug"
    permission_classes = [IsOwnerOrReadOnly]

class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [OrderingFilter]
    permission_classes = [AllowAny]
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        query_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            query_list = query_list.filter(
                Q(title__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return query_list
