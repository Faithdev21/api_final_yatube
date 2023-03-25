from posts.models import Comment, Follow, Group, Post, User
from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .permissions import IsAuthorOrAdmin
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Возвращает список постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Переопределение метода perform_create
        для сохранения автора при создании поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает информацию о группе."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrAdmin]


class CommentViewSet(viewsets.ModelViewSet):
    """Возвращает список комментариев к посту по id."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        """Переопределение метода perform_create
        для сохранения автора и id поста при создании комментария."""
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=self.kwargs.get('post_id'))
        )

    def get_queryset(self):
        """Переопределение метода get_queryset
        для запроса комментариев по id(pk) поста."""
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        ).comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    """Возвращает все подписки пользователя."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        """Переопределение метода get_queryset
        для запроса фолловеров по username."""
        user = get_object_or_404(
            User,
            username=self.request.user
        )
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        """Переопределение метода perform_create
        для сохранения фолловера при подписке на автора."""
        serializer.save(user=self.request.user)
