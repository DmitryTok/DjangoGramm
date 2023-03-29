from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from djangogramm_app.views import PostView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', PostView.as_view(), name='index'),
    path('djangogramm_app/', include('djangogramm_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
