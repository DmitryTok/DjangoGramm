from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View

from users.forms import UserRegisterForm


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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('index')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
