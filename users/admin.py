from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User


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


admin.site.unregister(Group)
