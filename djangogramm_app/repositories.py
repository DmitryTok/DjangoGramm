from django.shortcuts import get_object_or_404

from DjangoGramm.Base.base_repository import BaseRepository
from djangogramm_app import models


class PostRepository(BaseRepository):

    @property
    def model(self):
        return models.Post

    def get_all_posts(self):
        return self.model.objects.all().order_by('-pub_date')

    def get_post_by_id(self, post_id: int):
        return get_object_or_404(self.model, id=post_id)

    def delete_post_by_id(self, post_id: int) -> None:
        delete_post = get_object_or_404(self.model, id=post_id)
        delete_post.delete()

    def get_likes_or_dislikes(self, post_id: int, is_dislike=True):
        get_post = get_object_or_404(self.model, id=post_id)
        if is_dislike:
            return get_post.dislikes
        else:
            return get_post.likes


class PictureRepository(BaseRepository):

    @property
    def model(self):
        return models.Pictures


class TagRepository(BaseRepository):

    @property
    def model(self):
        return models.Tag
