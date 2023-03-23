from django.contrib import admin

from djangogramm_app.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'text',
        'picture',
        'pub_date'
    )
    list_filter = (
        'user',
        'text',
        'picture',
        'pub_date'
    )
    search_fields = (
        'user',
        'text',
        'picture',
        'pub_date'
    )
