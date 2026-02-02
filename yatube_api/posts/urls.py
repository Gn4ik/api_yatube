from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from .views import PostsViewSet, GroupViewSet, CommentViewSet

router_posts = SimpleRouter()
router_posts.register('posts', PostsViewSet)

router_groups = SimpleRouter()
router_groups.register('groups', GroupViewSet)

urlpatterns = [
  path('api-token-auth/', views.obtain_auth_token),
  path('', include(router_posts.urls)),
  path('', include(router_groups.urls)),
  path('posts/<int:post_id>/comments/', 
         CommentViewSet.as_view({
             'get': 'list',
             'post': 'create'
         })),
  path('posts/<int:post_id>/comments/<int:pk>/', 
         CommentViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
             'patch': 'partial_update',
             'delete': 'destroy'
         })),
]
