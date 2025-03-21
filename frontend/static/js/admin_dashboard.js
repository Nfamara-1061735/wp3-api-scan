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

function openModal(research) {
    document.getElementById("researchModalTitle").textContent = research.title;
    document.getElementById("researchModalBody").textContent = research.description;
    document.getElementById("researchStartDate").textContent = research.start_date;
    document.getElementById("researchEndDate").textContent = research.end_date;
    document.getElementById("researchLocation").textContent = research.location;
    document.getElementById("researchAgeRange").textContent = `${research.target_min_age} - ${research.target_max_age}`;
    document.getElementById("researchReward").textContent = research.has_reward ? research.reward : "Geen beloning";

    const limitationsList = document.getElementById("researchLimitations");
    limitationsList.innerHTML = "";
    if (research.limitations && research.limitations.length > 0) {
        research.limitations.forEach(limit => {
            const li = document.createElement("li");
            li.textContent = limit.limitation;
            limitationsList.appendChild(li);
        });
    } else {
        const list = document.createElement("li");
        list.textContent = "Geen beperkingen";
        limitationsList.appendChild(list);
    }

    const approveButton = document.getElementById("modalApproveButton");
    approveButton.onclick = () => approveResearch(research.research_id);

    const rejectButton = document.getElementById("modalRejectButton");
    rejectButton.onclick = () => rejectResearch(research.research_id);

    const modalElement = document.getElementById("researchModal");
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

function approveResearch(research_id) {
    fetch(`/api/researches/${research_id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status_id: 2 })
    })
    .then(response => {
        if (!response.ok) throw new Error("Goedkeuren niet gelukt.");
        return response.json();
    })
    .then(() => {
        showAlert("Onderzoek is goedgekeurd.", "success");
        bootstrap.Modal.getInstance(document.getElementById("researchModal")).hide();
        fetchResearches();
    })
    .catch(error => {
        console.error(error);
        showAlert("Goedkeuren mislukt.", "danger");
    });
}

function rejectResearch(research_id) {
    fetch(`/api/researches/${research_id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status_id: 3 })
    })
    .then(response => {
        if (!response.ok) throw new Error("Afkeuren niet gelukt.");
        return response.json();
    })
    .then(() => {
        showAlert("Onderzoek is afgekeurd.", "success");
        bootstrap.Modal.getInstance(document.getElementById("researchModal")).hide();
        fetchResearches();
    })
    .catch(error => {
        console.error(error);
        showAlert("Afkeuren mislukt.", "danger");
    });
}

/* ============= NEW PEER EXPERTS ============= */
function fetchNewPeerExperts() {
    fetch("/api/peers?sort_by=peer_expert_id&sort_order=asc")
        .then(response => response.json())
        .then(data => {
            const peerExperts = data.peer_experts.filter(peer => peer.peer_expert_status_id === 1);
            const tableBody = document.querySelector("#newPeerExpertsTable tbody");
            const message = document.getElementById("noNewPeerExpertsMessage");

            tableBody.innerHTML = "";

            if (peerExperts.length === 0) {
                message.classList.remove("d-none");
                return;
            } else {
                message.classList.add("d-none");
            }

            peerExperts.forEach(peer => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${peer.peer_expert_id}</td>
                    <td>${peer.user.first_name}</td>
                    <td>${peer.user.last_name}</td>
                    <td>${peer.postal_code}</td>
                    <td>${peer.gender}</td>
                    <td>${formatDate(peer.birth_date)}</td>
                    <td><button class="btn btn-info btn-sm" onclick="openPeerExpertModal(${peer.peer_expert_id})">Details</button></td>
                `;

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching peer experts:", error);
        });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    return date.toLocaleDateString('nl-NL', options);
}

function openPeerExpertModal(peerExpertId) {
    window.location.href = `/admin/peer-experts/${peerExpertId}`;
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