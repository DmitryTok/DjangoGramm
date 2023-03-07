from django.urls import path

from djangogramm_app.views import Avatar

urlpatterns = [
    path('picture/', Avatar.as_view(), name='avatar'),
]
