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


function showEditModal(currentPostId,currentTitle, currentBody,currentCountry,currentCategory,currentImage, currentFlag ){
    document.getElementById('edit-post-id').value = currentPostId;
    document.getElementById('edit-title').value = currentTitle;
    document.getElementById('edit-body').value = currentBody;
    document.getElementById('edit-country').value = currentCountry; 
    document.getElementById('edit-category').value = currentCategory;
    let postImage=document.getElementById('show-edit-post-img');
    let flagImage=document.getElementById('show-edit-flag-img');
    const uploadsPath = '/static/uploads/';


    if (currentFlag) {
        flagImage.src = `${uploadsPath}${currentFlag}`;
        flagImage.style.display = 'block'
        console.log(flagImage.src)
    } else {
        flagImage.src = ''; 
        flagImage.style.display = 'none';
    }

    let imageLabel = document.getElementById('edit-image-label');
    if (currentImage !='None') {
    postImage.src = `${uploadsPath}${currentImage}`;
    postImage.style.display = 'block';   // show image
    console.log(postImage.src);
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
    let country = document.getElementById('edit-country').value  
    let category = document.getElementById('edit-category').value;
    let postImage = document.getElementById('edit-post-img').files[0];
    let flagImage = document.getElementById('edit-flag-img').files[0];//for send the files 


    const formData = new FormData();
        formData.append('title', postTitle);
        formData.append('body', postBody);
        formData.append('post_id', postId);
        formData.append('country', country);
        formData.append('category', category);
        if (postImage) {
        formData.append('post_image', postImage);
        }
        if (flagImage) {
            formData.append('flag', flagImage);
        }

    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    editPost(formData ,postId)
    
}

function editPost(formData, postId){
    fetch(`/edit/${postId}`, {
        method: "POST" , 
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success){
            location.reload();
            $("#editPostModal").modal('hide');
            console.log('EDIT DONE')
            console.log(data)
        }
    })
}


// filter in global page 
const categoryFilter = document.getElementById('categoryFilter');
const countryFilter = document.getElementById('countryFilter');
const posts = document.querySelectorAll('.col-12.col-md-4'); 

function filterPosts() {
    const countrySelected = countryFilter.value
    const categorySelected = categoryFilter.value

    posts.forEach(post => {
        const postCountry = post.dataset.country || "";
        const postCategory = post.dataset.category || "";

        const matchCountry = !countrySelected || postCountry === countrySelected;
        
        const matchCategory = !categorySelected || postCategory === categorySelected;

        if (matchCountry && matchCategory) {
            post.style.display = "block";
        } else {
            post.style.display = "none";
        }
    });
}

countryFilter.addEventListener('change', filterPosts);
categoryFilter.addEventListener('change', filterPosts);


