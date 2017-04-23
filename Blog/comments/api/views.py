from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (
    AllowAny,
)
from serializers import CommentListSerializer, CommentDetailSerializer, create_comment_serializer
from posts.api.paginations import PostLimitOffsetPagination
from comments.models import Comment
from posts.api.permissions import IsOwnerOrReadOnly

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )

class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = "id"
    permission_classes = [IsOwnerOrReadOnly]

class CommentEditAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)  # override the all function that filters out comments that are not parent
    serializer_class = CommentDetailSerializer
    lookup_field = "id"
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.destroy(request,*args, **kwargs)

class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    filter_backends = [OrderingFilter]
    pagination_class = PostLimitOffsetPagination
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        query_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get("q")
        if query:
            query_list = query_list.filter(
                Q(title__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return query_list
