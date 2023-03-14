from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import View

from users.forms import (AvatarForm, CustomAuthenticationForm, ProfileForm,
                         UserRegisterForm)
from users.models import User
from users.utils import send_email_for_verify


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.is_email_veryfi = True
            user.save()
            login(request, user)
            return redirect('profile_settings')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class ProfileSettings(View):
    template_name = 'profiles/profile_settings.html'

    def get(self, request):
        context = {
            'profile_form': ProfileForm(request.POST, instance=request.user),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        profile_form = ProfileForm(request.POST, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        else:
            profile_form = ProfileForm(request.POST, instance=request.user)
        context = {
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)


class Profile(View):
    template_name = 'profiles/profile.html'

    def get(self, request):
        user = request.user
        context = {
            'user': user,
        }
        return render(request, self.template_name, context)


class UpdateProfile(View):
    template_name = 'profiles/update_profile.html'

    def get(self, request):
        context = {
            'common_form': UserRegisterForm(),
            'extra_fields_form': ProfileForm(),
            'avatar_form': AvatarForm()
        }
        return render(request, self.template_name, context)


class DeleteProfile(View):
    template_name = 'profiles/delete_profile.html'

    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, self.template_name, context)

    def post(self, request):
        request.user.delete()
        return redirect('index')
