fetch("https://jouw-api-url.com/api/data", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer jouw-api-key"
    },
    body: JSON.stringify({ data: "Jouw data hier" })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Error:", error));

