from django.urls import include, path
from django.views.generic import TemplateView

from users.views import (CustomLoginView, DeleteProfile, EmailVerify, Profile,
                         ProfileList, ProfileSettings, Register, UpdateProfile)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path(
        'invalid_verify/',
        TemplateView.as_view(template_name='registration/invalid_verify.html'),
        name='invalid_verify'
    ),
    path(
        'verify_email/<uidb64>/<token>/',
        EmailVerify.as_view(),
        name='verify_email'
    ),
    path('register/', Register.as_view(), name='register'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile_list/', ProfileList.as_view(), name='profile_list'),
    path('profile_page/', Profile.as_view(), name='profile_page'),
    path('update_profile/', UpdateProfile.as_view(), name='update_profile'),
    path('delete_profile/', DeleteProfile.as_view(), name='delete_profile'),
    path('profile_settings/', ProfileSettings.as_view(), name='profile_settings'),
    path(
        'confirm_email/',
        TemplateView.as_view(template_name='registration/confirm_email.html'),
        name='confirm_email'
    ),
    path('bad_request/', TemplateView.as_view(template_name='errors/400.html'), name='400')
]
