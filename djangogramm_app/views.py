from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
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
            post_form = PostForm(request.POST or None, request.FILES or None)
            if post_form.is_valid() and tag_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                tags_names = tag_form.cleaned_data['tags'].split(',')
                tags = []
                for tag_name in tags_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                    tags.append(tag)
                post.tags.set(tags)
                return redirect('index')
        else:
            post_form = PostForm(request.POST, request.FILES, instance=request.user.id)
            tag_form = TagForm(request.POST)
        context = {
            'post_form': post_form,
            'tag_form': tag_form
        }
        return render(request, self.template_name, context)


class UpdatePostView(View):
    template_name = 'posts/post_update.html'

    def get(self, request, post_id):
        if request.user.is_authenticated:
            current_post = Post.objects.get(id=post_id)
            post_form = PostForm(instance=current_post)
            tag_form = TagForm()
            context = {
                'post_form': post_form,
                'tag_form': tag_form,
                'current_post': current_post
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')

    def post(self, request, post_id):
        if request.user.is_authenticated:
            current_post = Post.objects.get(id=post_id)
            tag_form = TagForm(request.POST)
            post_form = PostForm(request.POST or None, request.FILES or None, instance=current_post)
            if post_form.is_valid() and tag_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                tags_names = tag_form.cleaned_data['tags'].split(',')
                tags = []
                for tag_name in tags_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                    tags.append(tag)
                post.tags.set(tags)
                messages.success(request, ('Your Post Has Been Updated'))
                return redirect('index')
            else:
                messages.success(request, ('You Must Be Loged In To View This Page'))
                return redirect('login')
        else:
            post_form = PostForm(request.POST, request.FILES)
            tag_form = TagForm(request.POST)
        context = {
            'post_form': post_form,
            'tag_form': tag_form
        }
        return render(request, self.template_name, context)


class DeletePostView(View):
    template_name = 'posts/post_delete.html'

    def get(self, request, post_id):
        if request.user.is_authenticated:
            post = Post.objects.get(id=post_id)
            context = {
                'post': post
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')

    def post(self, request, post_id):
        if request.user.is_authenticated:
            post = Post.objects.get(id=post_id)
            post.delete()
            messages.success(request, ('Your Post Has Been Deleted'))
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')
        return redirect('index')


class LikePostView(View):

    def get(self, request, post_id):
        return redirect('index')

    def post(self, request, post_id):
        if request.user.is_authenticated:
            post = get_object_or_404(Post, id=post_id)
            user = request.user
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
            return redirect('index')
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')
