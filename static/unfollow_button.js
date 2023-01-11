const unFollowButton = document.querySelector('#unfollow-button');
console.log(followButton);

unFollowButton.addEventListener('click', function userClick(evt) {
    evt.preventDefault();
    console.log("Button is clicked");
    

    const formInputs = { 
        user_handle: document.querySelector('#unfollow-user-handle').value   
    };
    console.log(formInputs)

    fetch('/unfollow', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })

        })
        .then((response) => response.json())
        .then((results) => {
            alert(results.status);
    });
