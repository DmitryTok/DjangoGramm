from django.urls import path

from djangogramm_app.views import (
    DeletePostView,
    LikePostView,
    PostCreateView,
    PostView,
    UpdatePostView,
)

urlpatterns = [
    path('', PostView.as_view(), name='index'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_update/<post_id>', UpdatePostView.as_view(), name='post_update'),
    path('post_delete/<post_id>', DeletePostView.as_view(), name='post_delete'),
    path('post_like/<post_id>', LikePostView.as_view(), name='post_like'),
]
