from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from djangogramm_app.forms import PictureFormPost, PostForm, TagForm
from djangogramm_app.utils import PICTURE_REPOSITORY, POST_REPOSITORY, add_dislike, add_like, tags


class PostView(View):
    template_name = 'index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        posts = POST_REPOSITORY.get_all_posts()
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
            messages.success(request, ('You Must Be Loged In To Create New Post'))
            return redirect('login')

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            picture_form = PictureFormPost(request.POST, request.FILES)
            tag_form = TagForm(request.POST)
            post_form = PostForm(request.POST or None, request.FILES or None)
            if post_form.is_valid() and tag_form.is_valid() and picture_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                tags_names = tag_form.cleaned_data['tags'].split(',')
                images = request.FILES.getlist('picture')
                imgs = []
                for img in images:
                    image = PICTURE_REPOSITORY.create(use_get_or_create=False, picture=img)
                    image.save()
                    imgs.append(image)
                post.tags.set(tags(tags_names))
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
        post = POST_REPOSITORY.get_post_by_id(post_id)
        if request.user.is_authenticated and post.user == request.user:
            context = {
                'post': post
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Cannot Delete Other Posts!'))
            return redirect('index')

    @staticmethod
    def post(request: HttpRequest, post_id: int) -> HttpResponse:
        post = POST_REPOSITORY.get_post_by_id(post_id)
        if request.user.is_authenticated and post.user == request.user:
            POST_REPOSITORY.delete_post_by_id(post_id)
            messages.success(request, ('Your Post Has Been Deleted!'))
        else:
            messages.success(request, ('You Must Be Loged In To View This Page!'))
            return redirect('login')
        return redirect('profile', request.user.id)


class LikePostView(View):

    @staticmethod
    def post(request: HttpRequest, post_id: int) -> HttpResponse:
        if request.user.is_authenticated:
            add_like(request, post_id)
            return redirect('index')
        else:
            messages.success(request, ('You Must Be Loged In To View This Page!'))
            return redirect('login')


class DisLikePostView(View):

    @staticmethod
    def post(request: HttpRequest, post_id: int) -> HttpResponse:
        if request.user.is_authenticated:
            add_dislike(request, post_id)
            return redirect('index')
        else:
            messages.success(request, ('You Must Be Loged In To View This Page!'))
            return redirect('login')
