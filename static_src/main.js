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
                    } else {
                        followButton.textContent = `Unfollow ${username}`;
                    }
                    updateButtonColor(followButton);
                })
                .catch(error => console.error(error));
        });
        updateButtonColor(followButton);
    }
});

function updateButtonColor(button) {
    const isFollowing = button.textContent.includes('Unfollow');

    if (isFollowing) {
        button.classList.remove('btn-success');
        button.classList.add('btn-danger');
    } else {
        button.classList.remove('btn-danger');
        button.classList.add('btn-success');
    }
}

document.addEventListener('DOMContentLoaded', () => {
  const likeButtons = document.querySelectorAll('.like-button');
  const dislikeButtons = document.querySelectorAll('.dislike-button');

  likeButtons.forEach(likeButton => {
    likeButton.addEventListener('click', () => {
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
          const dislikeButton = document.querySelector(`.dislike-button[data-post-id="${postId}"]`);
          if (dislikeButton) {
            dislikeButton.textContent = `Dislikes: ${data.dislikes_count}`;
            dislikeButton.classList.remove('btn-danger');
            dislikeButton.classList.add('btn-outline-danger');
          }

          likeButton.textContent = `Likes: ${data.likes_count}`;
          likeButton.classList.remove('btn-outline-primary');
          likeButton.classList.add('btn-primary');
        })
        .catch(error => console.error(error));
    });
  });

  dislikeButtons.forEach(dislikeButton => {
    dislikeButton.addEventListener('click', () => {
      const postId = dislikeButton.dataset.postId;
      const dislikeUrl = `/post_dislike/${postId}`;
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
          const likeButton = document.querySelector(`.like-button[data-post-id="${postId}"]`);
          if (likeButton) {
            likeButton.textContent = `Likes: ${data.likes_count}`;
            likeButton.classList.remove('btn-primary');
            likeButton.classList.add('btn-outline-primary');
          }

          dislikeButton.textContent = `Dislikes: ${data.dislikes_count}`;
          dislikeButton.classList.remove('btn-outline-danger');
          dislikeButton.classList.add('btn-danger');
        })
        .catch(error => console.error(error));
    });
  });
});
