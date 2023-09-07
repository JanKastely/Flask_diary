
  document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
      button.addEventListener('click', function () {
        const postId = this.getAttribute('data-post-id');
        console.log('Kliknuto na tlačítko "LIKE" pro příspěvek s ID:', postId);
        const likeCountElement = document.getElementById(`like-count-${postId}`);

        // Simulace inkrementace počtu "like"
        const currentLikes = parseInt(likeCountElement.innerText);
        likeCountElement.innerText = (currentLikes + 1).toString();

        // Provedení AJAX požadavku na server
        fetch(`/blog/like/${postId}`, { method: 'POST' })
          .then(response => response.json())
          .then(data => {
            likeCountElement.innerText = data.likes;
          })
          .catch(error => console.error('Chyba při like: ', error));

      });
    });
  });
