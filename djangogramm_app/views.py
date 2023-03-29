from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from djangogramm_app.forms import PostForm, TagForm
from djangogramm_app.models import Post, Tag


class PostView(View):
    template_name = 'index.html'

    def get(self, request):
        posts = Post.objects.all().order_by('-pub_date')
        context = {
            'posts': posts,
        }
        return render(request, self.template_name, context)


class PostCreateView(View):
    template_name = 'posts/post_create.html'

    def get(self, request):
        if request.user.is_authenticated:
            post_form = PostForm()
            tag_form = TagForm()
            context = {
                'post_form': post_form,
                'tag_form': tag_form
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            tag_form = TagForm(request.POST)
            post_form = PostForm(request.POST or None)
            if post_form.is_valid() and tag_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                tag_form.save()
                return redirect('index')
        else:
            post_form = PostForm(request.POST, request.FILES, instance=request.user.id)
            tag_form = TagForm(request.POST)
        context = {
            'post_form': post_form,
            'tag_form': tag_form
        }
        return render(request, self.template_name, context)
