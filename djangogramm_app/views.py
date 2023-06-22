from http import HTTPStatus
from typing import Union

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from djangogramm_app.forms import PictureFormPost, PostForm, TagForm
from djangogramm_app.repositories import PictureRepository, PostRepository
from djangogramm_app.utils import add_like_or_dislike, tags


class PostView(View):
    template_name = 'index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        post_repository = PostRepository()
        posts = post_repository.get_all_posts()
        user = request.user
        paginator = Paginator(posts, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'user': user,
            'posts': posts,
            'page_obj': page_obj
        }
        return render(request, self.template_name, context)


class PostCreateView(View):
    template_name = 'posts/post_create.html'

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
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

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        picture_repository = PictureRepository()
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
                    image = picture_repository.create(use_get_or_create=False, picture=img)
                    image.save()
                    imgs.append(image)
                post.tags.set(tags(tags_names))
                post.pictures.set(imgs)
                post_form.save_m2m()
                return redirect('index')
        else:
            messages.success(request, ('You Must Be Loged In To Create New Post'))
            return redirect('login')
        context = {
            'post_form': post_form,
            'tag_form': tag_form,
            'picture_form': picture_form
        }
        return render(request, self.template_name, context)


class DeletePostView(View):
    template_name = 'posts/post_delete.html'

    def get(self, request: HttpRequest, post_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        post_repository = PostRepository()
        post = post_repository.get_post_by_id(post_id)
        if request.user.is_authenticated and post.user == request.user:
            context = {
                'post': post
            }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('You Cannot Delete Other Posts!'))
            return redirect('index')

    @staticmethod
    def post(request: HttpRequest, post_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        post_repository = PostRepository()
        post = post_repository.get_post_by_id(post_id)
        if request.user.is_authenticated and post.user == request.user:
            post_repository.delete_post_by_id(post_id)
            messages.success(request, ('Your Post Has Been Deleted!'))
        else:
            messages.success(request, ('You Must Be Loged In To View This Page!'))
            return redirect('login')
        return redirect('profile', request.user.id)


class LikePostView(View):

    @staticmethod
    def post(request: HttpRequest, post_id: int) -> Union[JsonResponse, HttpResponse]:
        if request.user.is_authenticated:
            post_repository = PostRepository()
            add_like_or_dislike(request, post_id, is_liked=True)
            post = post_repository.get_post_by_id(post_id)
            response_data = {
                'likes_count': post.likes_count(),
                'dislikes_count': post.dislikes_count()
            }
            return JsonResponse(response_data, status=HTTPStatus.OK)
        else:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)


class DisLikePostView(View):

    @staticmethod
    def post(request: HttpRequest, post_id: int) -> Union[JsonResponse, HttpResponse]:
        if request.user.is_authenticated:
            post_repository = PostRepository()
            add_like_or_dislike(request, post_id, is_liked=False)
            post = post_repository.get_post_by_id(post_id)
            response_data = {
                'likes_count': post.likes_count(),
                'dislikes_count': post.dislikes_count()
            }
            return JsonResponse(response_data, status=HTTPStatus.OK)
        else:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
