
const followButton = document.querySelector('#follow-button');
console.log(followButton);

followButton.addEventListener('click', function userClick(evt) {
    evt.preventDefault();
    console.log("Button is clicked");
    

    const formInputs = { 
        user_handle: document.querySelector('#user-handle').value   
    };
    console.log(formInputs)

    fetch('/follow', {
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

            // if(followButton.innerText === 'Follow') {
            //     followButton.innerText = 'Unfollow';
            // } else {
            //     followButton.innerText = 'Follow';
            // }
    });
          


    


