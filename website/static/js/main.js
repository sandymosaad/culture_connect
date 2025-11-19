setTimeout(() => {
    const alerts = document.querySelectorAll('.my-alert');
    alerts.forEach(alert => {
        alert.style.display = 'none';
    });
}, 2000);

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
                statusParagraph.textContent = 'You haven\'t added any posts yet. Click "Add a Post" to create your first one!';
            }}
    })
};


function showEditModal(currentPostId, currentTitle, currentBody, currentCategory, currentPostImage ){
    document.getElementById('edit-post-id').value = currentPostId;
    document.getElementById('edit-title').value = currentTitle;
    document.getElementById('edit-body').value = currentBody;
    document.getElementById('edit-category').value = currentCategory;
    let postImage=document.getElementById('show-edit-post_image');
    const uploadsPath = '/static/uploads/';

    let imageLabel = document.getElementById('edit-image-label');
    if (currentPostImage !=null) {
        imageLabel.textContent = "Do you want to change image?";
        postImage.src = `${uploadsPath}${currentPostImage}`;
        postImage.style.display = 'block';   // show image
    } else {
        postImage.style.display = 'none';    // hide image
        imageLabel.textContent = "Do you want to upload image?";
    }
    $("#editPostModal").modal('show')

}

function submitEdit(){
    let postId = document.getElementById('edit-post-id').value ;
    let postTitle = document.getElementById('edit-title').value ;
    let postBody = document.getElementById('edit-body').value ;
    let category = document.getElementById('edit-category').value;
    let postImage = document.getElementById('edit-post_image').files[0];


    const formData = new FormData();
        formData.append('title', postTitle);
        formData.append('body', postBody);
        formData.append('id', postId);
        formData.append('category', category);
        if (postImage) {
        formData.append('post_image', postImage);
        }

    // for (let pair of formData.entries()) {
    //     console.log(pair[0] + ': ' + pair[1]);
    // }

    editPost(formData ,postId)
    
}

function editPost(formData, postId){
    fetch(`/edit/${postId}`, {
        method: "POST" , 
        body: formData,
        //console.log()
    })
    .then(res => res.json())
    .then(data => {
        if (data.success){
            location.reload();
            $("#editPostModal").modal('hide');
        }
    })
}
