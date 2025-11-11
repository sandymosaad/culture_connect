function deletePost(postId) {
    fetch(`/delete/${postId}`, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            console.log('donenennen')
            document.getElementById(`post-${postId}`).remove();
        }
    });
}
