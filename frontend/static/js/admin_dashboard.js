function removeElement(sender) {
    let element = sender.parentElement
    let accordionContent = element.parentElement

    // Remove element
    element.remove();

    // Add text if no more elements left
    if (accordionContent.childElementCount < 1) {
        let p = document.createElement("p");
        p.classList.add("text-muted");
        p.textContent = "Er zijn geen nieuwe elementen om goed te keuren.";

        accordionContent.appendChild(p);
    }
}

async function changeStatus(item_id, updated_status) {
    try {
        const response = await fetch('/researches', {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: { "item_id": item_id,
                    "updated_status": updated_status}
        });

        if (!response.ok) {
            console.log(Error(`${response.status}`))
        }

        const result = await response.json();
        console.log("Update Successful:", result);
    } catch(error) {
        console.error("Error updating item:", error);
    }
}
document.addEventListener("DOMContentLoaded", () => {
    fetchResearches();
    setInterval(fetchResearches, 5000);
})

function fetchResearches() {
    fetch("/dashboard_data")
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                    const researches = document.getElementById('researches');
                    researches.innerHTML = '';
                    const div = document.createElement('div');
                    div.className = 'research';
                    div.setAttribute('data-id', item.research_id);
                    if (item.data === '') {div.innerHTML = `
                                <div class="border rounded-3 p-3">
                                    <p>Geen openstaande onderzoeksvragen</p>
                                </div>`;}
                    else {div.innerHTML = `
                                <div class="border rounded-3 p-3">
                                    <p>Titel: ${item.title}</p>
                                    <p>Onderzoeksvraag ID: ${item.research_id}</p>
                                    <button onclick="changeStatus(${item.research_id}, 2)" class="btn btn-success me-2"
                                            aria-label="Approve expert registration 1">Goedkeuren
                                    </button>
                                    <button onclick="changeStatus(${item.research_id}, 3)" class="btn btn-danger"
                                            aria-label="Reject expert registration 1">Afkeuren
                                    </button>
                                </div>`}
                    researches.appendChild(div);
                    });
            })
        .catch(error => console.error("Error fetching data:", error))
}