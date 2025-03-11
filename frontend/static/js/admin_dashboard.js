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
                if (item.title === "researches") {
                    const researches = document.getElementById('researches');
                    researches.innerHTML = '';
                    data.forEach(research => {
                    const div = document.createElement('div');
                    div.className = 'research';
                    div.setAttribute('data-id', research.research_id);
                    if (research.data === '') {div.innerHTML = `
                                <div class="border rounded-3 p-3">
                                    <p>Geen openstaande onderzoeksvragen</p>
                                </div>`;} else {div.innerHTML = `
                                <div class="border rounded-3 p-3">
                                    <p>Titel: ${research.title}</p>
                                    <p>Onderzoeksvraag ID: ${research.research_id}</p>
                                    <button onclick="changeStatus(${research.research_id}, 2)" class="btn btn-success me-2"
                                            aria-label="Approve expert registration 1">Goedkeuren
                                    </button>
                                    <button onclick="changeStatus(${research.research_id}, 3)" class="btn btn-danger"
                                            aria-label="Reject expert registration 1">Afkeuren
                                    </button>
                                </div>`}

                    researches.appendChild(div);
                    });

                if (item.title === "peer_expert_registrations") {

                }

                if (item.title === "peer_experts") {

                }
                }
            })
        .catch(error => console.error("Error fetching data:", error))
})}