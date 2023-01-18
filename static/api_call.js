const authorLabel = document.querySelector('#author-label');
const quoteLabel = document.querySelector('#quote-label');



const options = {
	method: 'GET',
	headers: {
		'X-RapidAPI-Key': apiKey,
		'X-RapidAPI-Host': 'quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com'
	}
};

fetch('https://quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com/quote?token=ipworld.info', options)
	.then(response => response.json())
	.then((response) => {
		console.log(response);

		const author = response["author"];
		authorLabel.textContent = author;

		// pulling quote from response JSON
		const quote = response["text"];
		quoteLabel.textContent = quote;


	  });

