from django.urls import path
from .views import (
    ListCreatePostView, PostDetailView, LikePostAPIView, DislikePostAPIView
)

urlpatterns = [
    path('posts/', ListCreatePostView.as_view(), name="posts-list-create"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name="posts-detail"),
    path('posts/like/<int:pk>/', LikePostAPIView.as_view(), name='posts-like'),
    path('posts/dislike/<int:pk>/', DislikePostAPIView.as_view(), name='posts-dislike'),
]
