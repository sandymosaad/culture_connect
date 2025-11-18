
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
    let postImage=document.getElementById('show-edit-post-img');
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
    let postImage = document.getElementById('edit-post-img').files[0];


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
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success){
            location.reload();
            $("#editPostModal").modal('hide');
        }
    })
}


// filter in global page 
const categoryFilter = document.getElementById('categoryFilter');
const countryFilter = document.getElementById('countryFilter');
const posts = document.querySelectorAll('[data-country]'); 


function filterPosts() {
    const countrySelected = countryFilter.value
    const categorySelected = categoryFilter.value
    
    let isMatched=false;
    posts.forEach(post => {
        const postCountry = post.dataset.country || "";
        const postCategory = post.dataset.category || "";

        const matchCountry = !countrySelected || postCountry === countrySelected;
        
        const matchCategory = !categorySelected || postCategory === categorySelected;

        if (matchCountry && matchCategory) {
            isMatched = true
            post.classList.remove('d-none');
        } else {
            post.classList.add('d-none');
        }
    });
    const noPostsMess = document.getElementById('noPostsMess');
    if (!isMatched){
        noPostsMess.classList.remove('d-none')
    }
    else{
        noPostsMess.classList.add('d-none')
    }
}

countryFilter.addEventListener('change', filterPosts);
categoryFilter.addEventListener('change', filterPosts);

function addPostToFavorite(postId ){
    if(CURRENT_USER=='None'){
        const errorContainer = document.createElement('div');
        errorContainer.classList.add('my-alert' , 'error-alert')

        const errorElement = document.createElement('span');
        errorElement.textContent = 'You should login first to add favorite posts';
        errorContainer.appendChild(errorElement);
        // use [0] to access the first element in HTMLCollection
        const alertSection = document.getElementsByClassName('section-alert')[0];
        alertSection.appendChild(errorContainer)
        setTimeout(() => {
            errorContainer.style.display = 'none'
        }, 3000);
        return
    }
    let key = `favorites_${CURRENT_USER}`
    let icon =  document.getElementById(`favorite-${postId}`)
    let favorites = JSON.parse(localStorage.getItem(key)) || []

    if (icon.classList.contains('active')){
        icon.classList.remove("active")
        const index = favorites.indexOf(postId)
        if (index > -1){
            favorites.splice(index, 1);
        }
    }else{
        if(!favorites.includes(postId)){
        favorites.push(postId)
        icon.classList.add("active")
        }
    }

    localStorage.setItem(key , JSON.stringify(favorites))
}
function loadFavorites(){
    let key = `favorites_${CURRENT_USER}`
    let favorites = JSON.parse(localStorage.getItem(key)) || []
    if(favorites.length>0){
        favorites.forEach(postId => {
        let icon = document.getElementById(`favorite-${postId}`);
        if (icon) {
            icon.classList.add("active");
        }
    });
    }

}
document.addEventListener("DOMContentLoaded", loadFavorites);
