from typing import Type, Union

from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode

from DjangoGramm.base.base_repository import BaseRepository
from users import models


class UserRepository(BaseRepository):

    @property
    def model(self) -> Type[models.User]:
        return models.User

    def get(self) -> object:
        return self.model.objects.all()

    def get_user_id(self, user_id: int) -> models.User:
        return get_object_or_404(self.model, id=user_id)

    def get_request_user(self, request: HttpRequest) -> Union[HttpResponse, models.User]:
        return get_object_or_404(self.model, id=request.user.id)

    def delete_user_by_id(self, user_id: int) -> None:
        user = get_object_or_404(self.model, id=user_id)
        user.delete()

    def exclude_user(self, request: HttpRequest) -> Union[HttpResponse, models.User]:
        return self.model.objects.exclude(id=request.user.id)

    @staticmethod
    def get_user(uidb64: str) -> models.User:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(models.User, pk=uid)
        except (TypeError, ValueError, OverflowError,
                models.User.DoesNotExist, ValidationError):
            user = None
        return user

# TODO: make tests
    def get_followers_of_author(self, user_id: int) -> object:
        return self.model.objects.filter(follower__author_id=user_id)

    # TODO: make tests
    def get_count_followers_of_author(self, user_id: int) -> object:
        return self.model.objects.filter(follower__author_id=user_id).count()


class FollowRepository(BaseRepository):

    @property
    def model(self) -> Type[models.Follow]:
        return models.Follow

    def get_user_follow(self, user: int, user_id: int) -> Union[HttpResponse, models.Follow]:
        return self.model.objects.filter(user=user, author=user_id).exists()

    def get_unfollow_user(self, user: int, user_id: int) -> None:
        return self.model.objects.filter(user=user, author=user_id).delete()
