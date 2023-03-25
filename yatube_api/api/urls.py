from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet)
router_v1.register(r'groups', GroupViewSet)
router_v1.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router_v1.register(r'follow', FollowViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),  # Работа с токенами
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
