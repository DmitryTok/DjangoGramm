from django.urls import path

from djangogramm_app.views import PostView

urlpatterns = [
    path('', PostView.as_view(template_name='index.html'), name='index'),
]
