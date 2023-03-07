from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import View

from djangogramm_app.models import Avatar
from users.forms import CustomAuthenticationForm, ProfileForm, UserRegisterForm
from users.utils import send_email_for_verify

User = get_user_model()


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.is_email_verify = True
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
    template_name = 'registration/profile_settings.html'

    def get(self, request):
        context = {
            'form': ProfileForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = ProfileForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


# TODO Test profile page with avatar func
class Profile(View):
    template_name = 'profile.html'

    def get(self, request):
        user = request.user
        avatar = Avatar.objects.get(id=user)
        context = {
            'user': user,
            'avatar': avatar
        }
        return render(request, self.template_name, context)
