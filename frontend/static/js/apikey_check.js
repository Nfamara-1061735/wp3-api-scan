const apiKey = 'YOUR_API_KEY';
const url = 'https://api.example.com/endpoint';

fetch(url, {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${apiKey}`
    }
})
.then(response => {
    if (response.ok) {
        return response.json();
    } else {
        throw new Error('Invalid API key');
    }
})
.then(data => {
    console.log('API key is valid:', data);
})
.catch(error => {
    console.error('Error:', error.message);
});
