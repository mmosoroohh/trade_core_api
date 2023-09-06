"""Posts api Views."""

from rest_framework import generics

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.views import status
from rest_framework.response import Response

from .models import Post
from user_profile.models import Profile
from .serializers import PostSerializer


class ListCreatePostView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        """Create a post asynchronously"""
        post = Post.objects.create(
            title= request.data.get('title'), 
            description= request.data.get('description'),
            body =request.data.get('body'),
            user =request.user
        )

        return Response(
            data=PostSerializer(post).data,
            status=status.HTTP_200_OK
        )

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        try:
            post = self.queryset.get(pk=kwargs["pk"])
            return Response(PostSerializer(post).data)
        except Post.DoesNotExist:
            return Response(
                data={
                    "message" : "Post with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, *args, **kwargs):
        try:
            post = self.queryset.get(pk=kwargs["pk"])
            serializer = PostSerializer()
            update_post = serializer.update, post, request.data
            return Response(PostSerializer(update_post).data)
        except Post.DoesNotExist:
            return Response(
                data={
                    "message": "Post with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            post = self.queryset.get(pk=kwargs["pk"])
            post.delete
            return Response(status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
                data={
                    "message": "Post with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
            

class LikePostAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Like a post"""

    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def post(self, request,  *args, **kwargs):
        """Like a post."""
        post = self.queryset.get(pk=kwargs["pk"])
        username = request.user.username
        try:
            post.disliked_by.get(user__username__exact=username)
            # If it has been disliked before undislike it
            post.undislike_post(request.user.profile)
        except Profile.DoesNotExist:
            pass
        # Check if the post has been liked before
        try:
            post.liked_by.get(user__username__exact=username)
            # If it has been liked before unlike it
            post.unlike_post(request.user.profile)
            message = {"success": "Like cancelled successfully."}
            return Response(message, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            # If it has not been liked before like it
            post.like_post(request.user.profile)
            message = {"success": "Post liked successfully."}
            return Response(message, status=status.HTTP_200_OK)


class DislikePostAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Dislike a post."""

    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def post(self, request,  *args, **kwargs):
        """Dislike a  post."""
        post= self.queryset.get(pk=kwargs["pk"])
        username = request.user.username
        # Check if the post has been disliked before
        try:
            post.liked_by.get(user__username__exact=username)
            # If it has been disliked before undislike it
            post.unlike_post(request.user.profile)
        except Profile.DoesNotExist:
            pass

        try:
            post.disliked_by.get(user__username__exact=username)
            # If it has been disliked before undislike it
            post.undislike_post(request.user.profile)
            message = {"success": "Dislike cancelled successfully."}
            return Response(message, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            # If it has not been disliked before dislike it
            post.dislike_post(request.user.profile)
            message = {"success": "Post disliked successfully."}
            return Response(message, status=status.HTTP_200_OK)