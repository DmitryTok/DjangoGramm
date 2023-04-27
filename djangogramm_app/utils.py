from djangogramm_app.repositories import PictureRepository, PostRepository, TagRepository

POST_REPOSITORY = PostRepository()
TAG_REPOSITORY = TagRepository()
PICTURE_REPOSITORY = PictureRepository()


def tags(all_tags):
    tags_lst = []
    for post_tag in all_tags:
        tag, created = TAG_REPOSITORY.create(use_get_or_create=True, name=post_tag.strip())
        tags_lst.append(tag)
    return tags_lst


def add_like(request, post_id):
    like_post = POST_REPOSITORY.get_post_by_id(post_id)
    user = request.user
    if user in like_post.likes.all():
        like_post.likes.remove(user)
    else:
        like_post.likes.add(user)
        like_post.dislikes.remove(user)


def add_dislike(request, post_id):
    dislike_post = POST_REPOSITORY.get_post_by_id(post_id)
    user = request.user
    if user in dislike_post.dislikes.all():
        dislike_post.dislikes.remove(user)
    else:
        dislike_post.dislikes.add(user)
        dislike_post.likes.remove(user)
