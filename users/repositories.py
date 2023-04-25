from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode

from users.models import User


class UserRepository:
    model = User

    def get(self):
        return self.model.objects.all()

    def get_user_id(self, user_id: int):
        return get_object_or_404(self.model, id=user_id)

    def get_request_user(self, request: HttpRequest):
        return get_object_or_404(self.model, id=request.user.id)

    def delete_user_by_id(self, user_id: int) -> None:
        user = get_object_or_404(self.model, id=user_id)
        user.delete()

    def exclude_user(self, request: HttpRequest):
        return self.model.objects.exclude(id=request.user.id)

    @staticmethod
    def get_user(uidb64: str):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user
