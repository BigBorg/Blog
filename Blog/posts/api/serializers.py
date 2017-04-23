from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from posts.models import Post
from comments.models import Comment
from comments.api.serializers import CommentListSerializer

from accounts.api.serializers import UserDetailSerializer

detail_url = HyperlinkedIdentityField(
    view_name="posts-api:detail",
    lookup_field="slug"
)

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'published'
        ]


class PostListSerializer(ModelSerializer):
    url = detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'user',
            'title',
            'image',
            'content',
            'html',
            'published'
        ]

    def get_image(self,obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_html(self,obj):
        return obj.get_markdown()

class PostDetailSerializer(ModelSerializer):
    url = detail_url
    comments = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'user',
            'title',
            'slug',
            'content',
            'published',
            'comments'
        ]

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentListSerializer(c_qs, many=True, context={"request":self.context['request']}).data
        return comments