from django.shortcuts import get_object_or_404

from base_repository.repository import BaseRepository
from djangogramm_app.models import Pictures, Post, Tag


class PostRepository:

    @property
    def model(self):
        return Post

    def get_all_posts(self):
        return self.model.objects.all().order_by('-pub_date')

    def get_post_by_id(self, post_id: int):
        return get_object_or_404(self.model, id=post_id)

    def delete_post_by_id(self, post_id: int) -> None:
        delete_post = get_object_or_404(self.model, id=post_id)
        delete_post.delete()


class PictureRepository(BaseRepository):

    @property
    def model(self):
        return Pictures


class TagRepository(BaseRepository):

    @property
    def model(self):
        return Tag
