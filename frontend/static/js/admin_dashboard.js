document.addEventListener("DOMContentLoaded", function () {
    fetchResearches();
    fetchNewPeerExperts();

    setInterval(() => {
        fetchResearches();
        fetchNewPeerExperts();
    }, 10000);
});

/* ============= RESEARCHES ============= */
function fetchResearches() {
    fetch("/api/researches")
        .then(response => response.json())
        .then(data => {
            const approvalContainer = document.getElementById("researchApprovalContainer");
            approvalContainer.innerHTML = "";

            const newResearches = data.filter(research => research.status_id === 1);

            if (newResearches.length === 0) {
                approvalContainer.innerHTML = "<p class='text-muted'>Geen nieuwe onderzoeken om weer te geven.</p>";
                return;
            }

            newResearches.forEach(research => {
                const item = document.createElement("div");
                item.classList.add("border", "rounded-3", "p-3", "d-flex", "justify-content-between", "align-items-center");

                const title = document.createElement("p");
                title.classList.add("mb-0");
                title.textContent = research.title;

                const detailsButton = document.createElement("button");
                detailsButton.textContent = "Details";
                detailsButton.classList.add("btn", "btn-info", "me-2");
                detailsButton.setAttribute("aria-label", "Details bekijken");
                detailsButton.addEventListener("click", () => openModal(research));

                item.appendChild(title);
                item.appendChild(detailsButton);

                approvalContainer.appendChild(item);
            });
        })
        .catch(error => {
            console.error("Error fetching researches:", error);
        });
}

/* ============= PEER EXPERTS ============= */
function fetchNewPeerExperts() {
    fetch("/api/peers?sort_by=peer_expert_id&sort_order=asc")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("peerExpertApprovalContainer");
            container.innerHTML = "";

            const newPeerExperts = data.peer_experts.filter(peer => peer.peer_expert_status_id === 1);

            if (newPeerExperts.length === 0) {
                container.innerHTML = "<p class='text-muted'>Geen nieuwe ervaringsdeskundigen om weer te geven.</p>";
                return;
            }

            newPeerExperts.forEach(peer => {
                const card = document.createElement("div");
                card.classList.add("border", "rounded-3", "p-3", "d-flex", "justify-content-between", "align-items-center");

                const title = document.createElement("p");
                title.classList.add("mb-0");
                title.textContent = `${peer.user.first_name} ${peer.user.last_name} (${peer.postal_code})`;

                const buttonsDiv = document.createElement("div");

                const detailsButton = document.createElement("button");
                detailsButton.textContent = "Details";
                detailsButton.classList.add("btn", "btn-info", "me-2");
                detailsButton.addEventListener("click", () => openPeerExpertDetails(peer.peer_expert_id));

                const approveButton = document.createElement("button");
                approveButton.textContent = "Goedkeuren";
                approveButton.classList.add("btn", "btn-success", "me-2");
                approveButton.addEventListener("click", () => approvePeerExpert(peer.peer_expert_id));

                const rejectButton = document.createElement("button");
                rejectButton.textContent = "Afkeuren";
                rejectButton.classList.add("btn", "btn-danger");
                rejectButton.addEventListener("click", () => rejectPeerExpert(peer.peer_expert_id));

                buttonsDiv.appendChild(detailsButton);
                buttonsDiv.appendChild(approveButton);
                buttonsDiv.appendChild(rejectButton);

                card.appendChild(title);
                card.appendChild(buttonsDiv);

                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error("Error fetching peer experts:", error);
        });
}

/* ============= PEER EXPERT ACTIONS ============= */
function approvePeerExpert(peer_expert_id) {
    fetch(`/api/peers/${peer_expert_id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ peer_expert_status_id: 2 })
    })
    .then(response => {
        if (!response.ok) throw new Error("Goedkeuren mislukt.");
        return response.json();
    })
    .then(() => {
        showAlert("Ervaringsdeskundige is goedgekeurd.", "success");
        fetchNewPeerExperts();
    })
    .catch(error => {
        console.error(error);
        showAlert("Goedkeuren mislukt.", "danger");
    });
}

function rejectPeerExpert(peer_expert_id) {
    fetch(`/api/peers/${peer_expert_id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ peer_expert_status_id: 3 })
    })
    .then(response => {
        if (!response.ok) throw new Error("Afkeuren mislukt.");
        return response.json();
    })
    .then(() => {
        showAlert("Ervaringsdeskundige is afgekeurd.", "success");
        fetchNewPeerExperts();
    })
    .catch(error => {
        console.error(error);
        showAlert("Afkeuren mislukt.", "danger");
    });
}

function openPeerExpertDetails(peer_expert_id) {
    window.location.href = `/admin/peer-experts/${peer_expert_id}`; // Optional: direct link or open modal
}

/* ============= ALERT ============= */
function showAlert(message, type = "success") {
    const alertContainer = document.getElementById("alertContainer");

    alertContainer.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Sluiten"></button>
        </div>
    `;

    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.classList.remove("show");
            alert.classList.add("fade");
            setTimeout(() => alert.remove(), 500);
        }
    }, 3000);
}