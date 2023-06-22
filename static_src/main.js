$(document).ready(function() {
  $('.like-button, .unlike-button').click(function() {
    var button = $(this);
    var form = button.closest('form');

    $.ajax({
      type: 'POST',
      url: form.attr('action'),
      data: form.serialize(),
      success: function(response) {
        console.log('Like Request Successful');
        console.log(response);

        button.toggleClass('btn-outline-primary like-button btn-primary unlike-button');
        button.text('Likes: ' + response.likes_count);
        form.find('.dislike-button, .undislike-button').removeClass('btn-danger undislike-button').addClass('btn-outline-danger dislike-button');
        form.find('.dislike-button, .undislike-button').text('Dislikes: ' + response.dislikes_count);
      },
      error: function(xhr, status, error) {
        console.log('Like Request Error');
        console.log(error);
      }
    });
  });

  $('.dislike-button, .undislike-button').click(function() {
    var button = $(this);
    var form = button.closest('form');

    $.ajax({
      type: 'POST',
      url: form.attr('action'),
      data: form.serialize(),
      success: function(response) {
        console.log('Dislike Request Successful');
        console.log(response);

        button.toggleClass('btn-outline-danger dislike-button btn-danger undislike-button');
        button.text('Dislikes: ' + response.dislikes_count);
        form.find('.like-button, .unlike-button').removeClass('btn-primary unlike-button').addClass('btn-outline-primary like-button');
        form.find('.like-button, .unlike-button').text('Likes: ' + response.likes_count);
      },
      error: function(xhr, status, error) {
        console.log('Dislike Request Error');
        console.log(error);
      }
    });
  });
});
