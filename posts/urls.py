from django.urls import path
from .views import (
    ListCreatePostView, PostDetailView
)

urlpatterns = [
    path('posts/', ListCreatePostView.as_view(), name="posts-list-create"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name="posts-detail"),
]
