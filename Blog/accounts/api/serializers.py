from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
)
from rest_framework.serializers import EmailField, CharField

User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
        ]


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email address")  # To override default nullable feature
    email2 = EmailField(label="Confirm email")
    class Meta:
        model = User
        fields=[
            'username',
            'password',
            'email',
            'email2'
        ]
        extra_kwargs={
            "password":{"write_only":True}
        }

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1!=email2:
            raise ValidationError("Emails must match!")
        return value

    def validate_email(self, attrs):
        if User.objects.filter(email=attrs.get("email")).exists():
            raise ValidationError("This email has already registered.")
        return attrs

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        email = validated_data.get("email")
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    email = EmailField(label = "Email address", allow_blank=True, required=False)

    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password',
            'token'
        ]
        extra_kwargs={
            "password":{"write_only": True}
        }

    def validate(self, attrs):
        user_obj = None
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")
        if not email and not username:
            raise ValidationError("A username or email is required to login!")

        user = User.objects.filter(
            Q(username=username) |
            Q(email=email)
        ).distinct()
        user = user.exclude(email__isnull=True)
        if user.exists() and user.count()==1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid!")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again.")
        attrs['token'] = "Logged in"
        return attrs