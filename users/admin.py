from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import Follow, User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
    )
    list_filter = (
        'email',
        'username',
    )
    search_fields = (
        'email',
        'username',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    list_filter = (
        'user',
        'author',
    )
    search_fields = (
        'user',
        'author',
    )


admin.site.unregister(Group)
