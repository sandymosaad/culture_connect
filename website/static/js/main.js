function deletePost(postId) {
    fetch(`/delete/${postId}`, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`post-${postId}`).remove();
            // change the para if user delete all posts 
            const remainingPosts = document.querySelectorAll('.card[id^="post-"]').length; 
            const statusParagraph = document.querySelector('.checkRemainingPostsPar');
            if (remainingPosts==0){
                statusParagraph.textContent = "You haven't added any posts yet. Click 'Add a Post' to get started!";
            }


        }
    });
}

