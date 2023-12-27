slider.addEventListener('click', e => {
    let button = e.target;
    if (button.classList.contains('post_like')) {
        if (button.classList.contains('liked')) {
            button.classList.toggle("liked");
            button.src = "../img/notLike.png";
        }
        else {
            button.classList.toggle("liked");
            button.src = "../img/Like.png";

            let dislikeButton = button.closest(".post_feedback").querySelector(".dislike_info").querySelector(".post_dislike_button").querySelector(".post_dislike");

            if (dislikeButton.classList.contains('disliked')) {
                dislikeButton.classList.toggle("disliked");
                dislikeButton.src = "../img/notDislike.png";
            }
        }
    }

    if (button.classList.contains('post_dislike')) {
        if (button.classList.contains('disliked')) {
            button.classList.toggle("disliked");
            button.src = "../img/notDislike.png";
        }
        else {
            button.classList.toggle("disliked");
            button.src = "../img/Dislike.png";

            let likeButton = button.closest(".post_feedback").querySelector(".like_info").querySelector(".post_like_button").querySelector(".post_like");;

            if (likeButton.classList.contains('liked')) {
                likeButton.classList.toggle("liked");
                likeButton.src = "../img/notLike.png";
            }

        }
    }
});


