const getCookie = name => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
};

const getProfileData = (userId) => {
  const profileUrl = `http://localhost:8000/users/profile/${userId}`;

  fetch(profileUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      return response.text();
    })
    .then(data => {
      console.log(data);
    })
    .catch(error => console.error(error));
};

const handleFollow = () => {
  const followButton = document.querySelector('#form_ajax_follow .follow-button');
  const userId = followButton.dataset.followId;
  const followUrl = `http://localhost:8000/users/profile_follow/${userId}`;
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
      return response.json();
    })
    .then(data => {
      console.log(data);
      followButton.textContent = `Unfollow ${username}`;
      followButton.classList.remove('btn-outline-success');
      followButton.classList.add('btn-outline-danger');

      getProfileData(userId);
    })
    .catch(error => console.error(error));
};

const handleUnfollow = () => {
  const unfollowButton = document.querySelector('#form_ajax_unfollow .unfollow-button');
  const userId = unfollowButton.dataset.unfollowId;
  const unfollowUrl = `http://localhost:8000/users/profile_unfollow/${userId}`;
  const username = unfollowButton.dataset.userUsername;
  const httpHeaders = {
    'Content-type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken'),
  };

  fetch(unfollowUrl, {
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
      unfollowButton.textContent = `Follow ${username}`;
      unfollowButton.classList.remove('btn-outline-danger');
      unfollowButton.classList.add('btn-outline-success');

      getProfileData(userId);
    })
    .catch(error => console.error(error));
};

$(document).ready(function() {
  $("#form_ajax_follow .follow-button").click(function() {
    handleFollow();
  });

  $("#form_ajax_unfollow .unfollow-button").click(function() {
    handleUnfollow();
  });
});
