from django.urls import path

from djangogramm_app.views import PostCreateView, PostView

urlpatterns = [
    path('', PostView.as_view(), name='index'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
]
