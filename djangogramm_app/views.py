from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from djangogramm_app.models import Post


class PostView(View):
    template_name = 'index.html'

    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.all()
            context = {
                'posts': posts
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')
