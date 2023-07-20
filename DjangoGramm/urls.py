from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('djangogramm_app.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
