from django.urls import path

from djangogramm_app.views import (
    DeletePostView,
    DisLikePostView,
    LikePostView,
    PostCreateView,
    PostView,
)

urlpatterns = [
    path('', PostView.as_view(), name='index'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_delete/<post_id>', DeletePostView.as_view(), name='post_delete'),
    path('post_like/<post_id>', LikePostView.as_view(), name='post_like'),
    path('post_dislike/<post_id>', DisLikePostView.as_view(), name='post_dislike'),
]
