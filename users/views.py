from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import View

from djangogramm_app.models import Pictures, Post
from email_veryfi.send_email_for_verify import send_email_for_verify
from users.forms import (
    CustomAuthenticationForm,
    PictureFormAvatar,
    ProfileForm,
    UserRegisterForm,
    UserUpdateForm,
)
from users.models import User


# TODO: Finish reset password func
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm


class EmailVerify(View):

    def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.is_email_verify = True
            user.save()
            login(request, user)
            return redirect('profile_settings')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64: str) -> User:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': UserRegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class ProfileSettings(View):
    template_name = 'profiles/profile_settings.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'profile_form': ProfileForm(instance=request.user),
            'profile_avatar_form': PictureFormAvatar(instance=request.user.avatar)
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        profile_form = ProfileForm(request.POST, instance=request.user)
        profile_avatar_form = PictureFormAvatar(
            request.POST or None,
            request.FILES or None,
            instance=request.user.avatar
        )

        if profile_form.is_valid() and profile_avatar_form.is_valid():
            profile_form.save(commit=False)
            avatar = request.FILES.get('picture')
            if avatar:
                image = Pictures(picture=avatar)
                image.save()
                request.user.avatar = image
            profile_form.save()
            return redirect('profile', request.user.id)
        else:
            profile_avatar_form = PictureFormAvatar(
                request.POST or None,
                request.FILES or None,
                instance=request.user.avatar
            )
            profile_form = ProfileForm(request.POST, instance=request.user)
        context = {
            'profile_form': profile_form,
            'profile_avatar_form': profile_avatar_form
        }
        return render(request, self.template_name, context)


class Profile(View):
    template_name = 'profiles/profile.html'

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        if request.user.is_authenticated:
            user = User.objects.get(id=user_id)
            posts = Post.objects.filter(user__id=user_id).order_by('pub_date')
            post_count = Post.objects.filter(user__id=user_id).count()
            context = {
                'user': user,
                'posts': posts,
                'post_count': post_count
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')


class UpdateProfile(View):
    template_name = 'profiles/update_profile.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            current_user = User.objects.get(id=request.user.id)
            context = {
                'extra_fields_form': ProfileForm(instance=current_user),
                'common_form': UserUpdateForm(instance=current_user),
                'profile_avatar_form': PictureFormAvatar(instance=request.user.avatar)
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            current_user = User.objects.get(id=request.user.id)
            common_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=current_user)
            extra_fields_form = ProfileForm(
                request.POST or None,
                request.FILES or None,
                instance=current_user
            )
            profile_avatar_form = PictureFormAvatar(
                request.POST or None,
                request.FILES or None,
                instance=current_user.avatar)
            if common_form.is_valid() and extra_fields_form.is_valid() and profile_avatar_form.is_valid():
                common_form.save()
                extra_fields_form.save(commit=False)
                avatar = request.FILES.get('picture')
                if avatar:
                    image = Pictures(picture=avatar)
                    image.save()
                    current_user.avatar = image
                    current_user.save()
                    extra_fields_form.save()
                messages.success(request, ('Your profile has been updated'))
                return redirect('index')
            else:
                context = {
                    'extra_fields_form': extra_fields_form,
                    'common_form': common_form,
                    'profile_avatar_form': profile_avatar_form
                }
                return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')


class DeleteProfile(View):
    template_name = 'profiles/delete_profile.html'

    def get(self, request: HttpRequest, user_id) -> HttpResponse:
        user = User.objects.get(id=user_id)
        if request.user.is_authenticated and user == request.user:
            context = {
                'user': user
            }
            return render(request, self.template_name, context)
        else:
            messages.error(request, ('You Cannot Delete Other Profiles!'))
            return redirect('login')

    @staticmethod
    def post(request: HttpRequest, user_id) -> HttpResponse:
        user = User.objects.get(id=user_id)
        if request.user.is_authenticated and user == request.user:
            user.delete()
            messages.success(request, ('Your Profile Has Been Deleted!'))
        else:
            messages.success(request, ('You Must Be Loged In To View This Page!'))
            return redirect('login')
        return redirect('index')


class ProfileList(View):
    template_name = 'profiles/profile_list.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            all_users = User.objects.exclude(id=request.user.id)
            context = {
                'all_users': all_users,
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')
