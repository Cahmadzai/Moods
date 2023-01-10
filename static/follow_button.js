
const followButton = document.getElementById('follow-button');

followButton.addEventListener('click', function userClick() {
    if(followButton.innerText === 'Follow') {
        followButton.innerText = 'Unfollow';
    } else {
        followButton.innerText = 'Follow';
    }

    const formInputs = { 
        user_handle: document.querySelector('#element').value   
    };

    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    
        .then((response) => response.json())
        .then((responseJson) => {
            alert(responseJson.status);
        });      
});

