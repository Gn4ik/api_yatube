from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from posts.models import Post, Group, Comment
from posts.serializers import (PostSerializer,
                               GroupSerializer, CommentSerializer)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'detail': 'У вас нет прав для редактирования этого поста.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'detail': 'У вас нет прав для удаления этого поста.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def get_comments(self, request, pk=None):
        """Получить или создать комментарии для поста"""
        post = self.get_object()

        if request.method == 'GET':
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {'detail': 'У вас нет прав для '
                    'редактирования этого комментария.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {'detail': 'У вас нет прав для '
                    'редактирования этого комментария.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {'detail': 'У вас нет прав для удаления этого комментария.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
