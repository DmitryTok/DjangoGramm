from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from djangogramm_app.forms import PictureFormPost, PostForm, TagForm
from djangogramm_app.models import Pictures, Post, Tag


class PostView(View):
    template_name = 'index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        posts = Post.objects.all().order_by('-pub_date')
        user = request.user
        context = {
            'user': user,
            'posts': posts,
        }
        return render(request, self.template_name, context)


class PostCreateView(View):
    template_name = 'posts/post_create.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            picture_form = PictureFormPost()
            post_form = PostForm()
            tag_form = TagForm()
            context = {
                'post_form': post_form,
                'tag_form': tag_form,
                'picture_form': picture_form
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            picture_form = PictureFormPost(request.POST, request.FILES)
            tag_form = TagForm(request.POST)
            post_form = PostForm(request.POST or None, request.FILES or None)
            images = request.FILES.getlist('picture')
            if post_form.is_valid() and tag_form.is_valid() and picture_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                tags_names = tag_form.cleaned_data['tags'].split(',')
                tags = []
                imgs = []
                for tag_name in tags_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                    tags.append(tag)
                for img in images:
                    image = Pictures(picture=img)
                    image.save()
                    imgs.append(image)
                post.tags.set(tags)
                post.pictures.set(imgs)
                post_form.save_m2m()
                return redirect('index')
        else:
            post_form = PostForm(request.POST, request.FILES, instance=request.user.id)
            tag_form = TagForm(request.POST)
            picture_form = PictureFormPost(request.POST, request.FILES)
        context = {
            'post_form': post_form,
            'tag_form': tag_form,
            'picture_form': picture_form
        }
        return render(request, self.template_name, context)


class UpdatePostView(View):
    template_name = 'posts/post_update.html'

    def get(self, request: HttpRequest, post_id: int) -> HttpResponse:
        if request.user.is_authenticated:
            current_post = Post.objects.get(id=post_id)
            picture_form = PictureFormPost()
            post_form = PostForm(instance=current_post)
            tag_form = TagForm()
            context = {
                'post_form': post_form,
                'tag_form': tag_form,
                'picture_form': picture_form
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            picture_form = PictureFormPost(request.POST, request.FILES)
            tag_form = TagForm(request.POST)
            post_form = PostForm(request.POST or None, request.FILES or None)
            images = request.FILES.getlist('picture')
            if post_form.is_valid() and tag_form.is_valid() and picture_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                tags_names = tag_form.cleaned_data['tags'].split(',')
                tags = []
                imgs = []
                for tag_name in tags_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                    tags.append(tag)
                for img in images:
                    image = Pictures(picture=img)
                    image.save()
                    imgs.append(image)
                post.tags.set(tags)
                post.pictures.set(imgs)
                post_form.save_m2m()
                return redirect('index')
        else:
            post_form = PostForm(request.POST, request.FILES, instance=request.user.id)
            tag_form = TagForm(request.POST)
            picture_form = PictureFormPost(request.POST, request.FILES)
        context = {
            'post_form': post_form,
            'tag_form': tag_form,
            'picture_form': picture_form
        }
        return render(request, self.template_name, context)


class DeletePostView(View):
    template_name = 'posts/post_delete.html'

    def get(self, request: HttpRequest, post_id: int) -> HttpResponse:
        if request.user.is_authenticated:
            post = Post.objects.get(id=post_id)
            context = {
                'post': post
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')

    def post(self, request: HttpRequest, post_id: int) -> HttpResponse:
        if request.user.is_authenticated:
            post = Post.objects.get(id=post_id)
            post.delete()
            messages.success(request, ('Your Post Has Been Deleted'))
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')
        return redirect('index')


class LikePostView(View):

    def post(self, request: HttpRequest, post_id: int) -> HttpResponse:
        if request.user.is_authenticated:
            like_post = get_object_or_404(Post, id=post_id)
            user = request.user
            if user in like_post.likes.all():
                like_post.likes.remove(user)
                return redirect('index')
            else:
                like_post.likes.add(user)
            return redirect('index')
        else:
            messages.success(request, ('You Must Be Loged In To View This Page'))
            return redirect('login')
