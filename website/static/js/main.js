function deletePost(postId) {
    fetch(`/delete/${postId}`, {method: "POST"})
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`post-${postId}`).remove();
            // change the para if user delete all posts 
            const remainingPosts = document.querySelectorAll('.card[id^="post-"]').length; 
            const statusParagraph = document.querySelector('.checkRemainingPostsPar');
            if (remainingPosts==0){
                statusParagraph.textContent = "You haven't added any posts yet. Click 'Add a Post' to get started!";
            }}
    })
};

function showEditModal(currentPostId,currentTitle, currentBody,currentCountry,currentCategory,currentImage, currentFlag ){
    document.getElementById('edit-title').value = currentTitle;
    document.getElementById('edit-body').value = currentBody;
    document.getElementById('edit-country').value = currentCountry; 
    document.getElementById('edit-category').value = currentCategory;
    let postImage=document.getElementById('edit-post-img');
    let flagImage=document.getElementById('edit-flag-img');

    const uploadsPath = '/static/uploads/';

    if (currentFlag) {
        flagImage.src = `${uploadsPath}${currentFlag}`;
        flagImage.style.display = 'block'
        console.log(flagImage.src)
    } else {
        flagImage.src = ''; 
        flagImage.style.display = 'none';
    }
    if (currentImage) {
        postImage.src = `${uploadsPath}${currentImage}`;
        postImage.style.display = 'block'
        console.log(postImage.src)
    } else {
        postImage.src = '';
        postImage.style.display = 'none';
    }
    $("#editPostModal").modal('show')

}
// function editPost(postId){
//     fetch(`/edit/${postId}`, {method: "POST"})
//     .then(res => res.json())
//     .then(data => {
//         if (data.success){

//             open.model('addPostModalLabel')
//             console.log('EDIT DONE')
//             console.log(data)
//         }
//     })
// }


