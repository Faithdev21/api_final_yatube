import base64
import uuid

from django.core.files.base import ContentFile
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


class Base64ImageField(serializers.ImageField):
    """Кодировка изображений в формате base64."""
    def to_internal_value(self, data) -> uuid.UUID:
        """Ввод является допустимой строкой UUID"""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields: tuple[str] = ('author', 'pub_date',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор групп."""
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields: tuple[str] = ('slug',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields: tuple[str] = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    validators = [
        UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following'])
    ]

    def validate(self, data):
        """Отсутствие возможности подписаться на себя."""
        if self.context.get('request').user != data.get('following'):
            return data
        raise serializers.ValidationError(
            'Нельзя подписаться на себя'
        )

    class Meta:
        model = Follow
        fields = '__all__'
