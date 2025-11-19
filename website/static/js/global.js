
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
if(countryFilter && categoryFilter) {
    countryFilter.addEventListener('change', filterPosts);
    categoryFilter.addEventListener('change', filterPosts);
}

function addPostToFavorite(postId ){
    if(CURRENT_USER=='None' || CURRENT_USER==undefined ){
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
