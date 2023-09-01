"""Posts api Views."""

from rest_framework import generics

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.views import status
from rest_framework.response import Response
import asyncio

from .models import Post
from .serializers import PostSerializer


class ListCreatePostView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    async def post(self, request, *args, **kwargs):
        """Create a post asynchronously"""
        post = await asyncio.to_thread(Post.objects.get, pk=kwargs["pk"])
        
        serializer = PostSerializer(
            data={
                "title": request.data.get('title'), 
                "description": request.data.get('description'),
                "body": request.data.get('body'),
                "user": request.user
            }
        )
        
        if serializer.is_valid():
            async def save_serializer():
                return await asyncio.to_thread(
                    serializer.save,
                    title=request.data.get('title'),
                    description=request.data.get('description'),
                    body=request.data.get('body'),
                    user=request.user
                )
            
            data = await save_serializer()
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    async def get(self, request, *args, **kwargs):
        try:
            post = await asyncio.to_thread(self.queryset.get, pk=kwargs["pk"])
            return Response(PostSerializer(post).data)
        except Post.DoesNotExist:
            return Response(
                data={
                    "message" : "Post with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    async def put(self, request, *args, **kwargs):
        try:
            post = await asyncio.to_thread(self.queryset.get, pk=kwargs["pk"])
            serializer = PostSerializer()
            update_post = await asyncio.to_thread(serializer.update, post, request.data)
            return Response(PostSerializer(update_post).data)
        except Post.DoesNotExist:
            return Response(
                data={
                    "message": "Post with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    async def delete(self, request, *args, **kwargs):
        try:
            post = await asyncio.to_thread(self.queryset.get, pk=kwargs["pk"])
            await asyncio.to_thread(post.delete)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response(
                data={
                    "message": "Post with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
            