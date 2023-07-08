    function getCookie(name) {
        const cookieValue = document.cookie.split('; ')
            .find(cookie => cookie.startsWith(name + '='))
            .split('=')[1];
        return cookieValue;
    }

    document.addEventListener('DOMContentLoaded', () => {
        const followButton = document.querySelector('.follow-button');

        if (followButton) {
            followButton.addEventListener('click', () => {
                const isFollowing = followButton.textContent.includes('Unfollow');
                const userId = followButton.dataset.followId;
                const followUrl = isFollowing
                    ? `http://localhost:8000/users/profile_unfollow/${userId}`
                    : `http://localhost:8000/users/profile_follow/${userId}`;
                const username = followButton.dataset.userUsername;
                const httpHeaders = {
                    'Content-type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                };

                fetch(followUrl, {
                    method: 'POST',
                    headers: httpHeaders,
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`Error: ${response.status} ${response.statusText}`);
                        }
                        console.log(response);
                        return response.text();
                    })
                    .then(data => {
                        console.log(data);
                        if (isFollowing) {
                            followButton.textContent = `Follow ${username}`;
                            followButton.classList.remove('btn-danger');
                            followButton.classList.add('btn-success');

                        } else {
                            followButton.textContent = `Unfollow ${username}`;
                            followButton.classList.remove('btn-success');
                            followButton.classList.add('btn-danger');

                        }
                    })
                    .catch(error => console.error(error));
            });
        }
    });
document.addEventListener('DOMContentLoaded', () => {
  const likeButtons = document.querySelectorAll('.like-button');
  const dislikeButtons = document.querySelectorAll('.dislike-button');

  likeButtons.forEach(likeButton => {
    likeButton.addEventListener('click', () => {
      const isLiked = likeButton.classList.contains('btn-primary');
      const postId = likeButton.dataset.postId;
      const likeUrl = `/post_like/${postId}`;
      const httpHeaders = {
        'Content-type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      };

      fetch(likeUrl, {
        method: 'POST',
        headers: httpHeaders,
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
          }
          return response.json();
        })
        .then(data => {
          likeButton.textContent = `Likes: ${data.likes_count}`;
          likeButton.classList.toggle('btn-primary');
          likeButton.classList.toggle('btn-outline-primary');
        })
        .catch(error => console.error(error));
    });
  });

  dislikeButtons.forEach(dislikeButton => {
    dislikeButton.addEventListener('click', () => {
      const isDisliked = dislikeButton.classList.contains('btn-danger');
      const postId = dislikeButton.dataset.postId;
      const dislikeUrl = `post_dislike/${postId}`;
      const httpHeaders = {
        'Content-type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      };

      fetch(dislikeUrl, {
        method: 'POST',
        headers: httpHeaders,
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
          }
          return response.json();
        })
        .then(data => {
          dislikeButton.textContent = `Dislikes: ${data.dislikes_count}`;
          dislikeButton.classList.toggle('btn-danger');
          dislikeButton.classList.toggle('btn-outline-danger');
        })
        .catch(error => console.error(error));
    });
  });
});
