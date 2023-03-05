from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import UserCreationForm

User = get_user_model()


@admin.register(User)
class UsersAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    add_form = UserCreationForm
    list_display = ('id', 'username', 'email', 'is_email_verify', 'full_name', 'bio')
    list_filter = ('id', 'username', 'email', 'is_email_verify', 'full_name', 'bio')
    search_fields = ('id', 'username', 'email', 'is_email_verify', 'full_name', 'bio')
    ordering = ('username',)
