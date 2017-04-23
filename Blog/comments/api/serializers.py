from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    HyperlinkedIdentityField
)
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer
comment_url = HyperlinkedIdentityField(view_name="comments-api:thread",lookup_field="id")

User = get_user_model()
def create_comment_serializer(model_type="post", slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            self.user = user
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count()==1:
                    self.parent_obj = parent_qs.first()
            super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count()!=1:
                raise ValidationError("This is not a valid content type.")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count()!=1:
                raise ValidationError("This is not a slug for this content type.")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            user = self.user
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(model_type,slug,content,user,parent_obj)
            return comment

    return CommentCreateSerializer



class CommentListSerializer(ModelSerializer):
    reply_count = SerializerMethodField(read_only=True)
    user = UserDetailSerializer()
    url = comment_url
    # post = post_url
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'url',
            'timestamp',
            'reply_count',
            'content',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        else:
            return 0

class CommentChildSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
        ]

class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField(read_only=True)
    user = UserDetailSerializer(read_only=True)
    content_object_url = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'reply_count',
            'timestamp',
            'replies',
            'content_object_url'
        ]
        read_only_fields=[
            'id',
            'reply_count',
            'timestamp',
            'replies'
        ]

    def get_content_object_url(self, obj):
        return obj.content_object.get_api_url()

    def get_replies(self,obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        else:
            return 0