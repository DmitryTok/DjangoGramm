from djangogramm_app.repositories import PostRepository, TagRepository


def tags(all_tags):
    tag_repository = TagRepository()
    tags_lst = []
    for post_tag in all_tags:
        tag, created = tag_repository.create(use_get_or_create=True, name=post_tag.strip())
        tags_lst.append(tag)
    return tags_lst


def add_like_or_dislike(request, post_id, is_liked=True):
    post_repository = PostRepository()
    like_post = post_repository.get_likes_or_dislikes(post_id, is_dislike=False)
    dislike_post = post_repository.get_likes_or_dislikes(post_id, is_dislike=True)
    user = request.user
    if is_liked:
        if like_post.filter(id=user.id).exists():
            like_post.remove(user)
        else:
            like_post.add(user)
            dislike_post.remove(user)
    else:
        if dislike_post.filter(id=user.id).exists():
            dislike_post.remove(user)
        else:
            dislike_post.add(user)
            like_post.remove(user)
