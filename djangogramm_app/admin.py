from django.contrib import admin

from djangogramm_app.models import Pictures, Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'text',
        'pub_date',
    )
    list_filter = (
        'user',
        'text',
        'pub_date',
    )
    search_fields = (
        'user',
        'text',
        'pub_date',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_filter = (
        'id',
        'name',
    )
    search_fields = (
        'id',
        'name',
    )


@admin.register(Pictures)
class PictureAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'picture',
    )
    list_filter = (
        'id',
        'picture',
    )
    search_fields = (
        'id',
        'picture',
    )
