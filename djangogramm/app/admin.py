from django.contrib import admin

from .models import DGUser, Like, Picture, Post, PostTag, Tag


@admin.register(DGUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'password',
        'full_name',
        'bio',
        'avatar'
    )
    search_fields = ('id', 'email', 'full_name')
    list_filter = ('id', 'email', 'full_name')


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ('id', 'image')
    list_filter = ('id', 'image')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('id', 'name', 'slug')
    list_filter = ('id', 'name', 'slug')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'tags', 'image')
    search_fields = ('id', 'text', 'tags', 'image')
    list_filter = ('id', 'text', 'tags', 'image')


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'tag_id')
    search_fields = ('id', 'post_id', 'tag_id')
    list_filter = ('id', 'post_id', 'tag_id')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'post_id', 'is_like')
    search_fields = ('id', 'user_id', 'post_id', 'is_like')
    list_filter = ('id', 'user_id', 'post_id', 'is_like')
