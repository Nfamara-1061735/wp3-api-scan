document.addEventListener("DOMContentLoaded", function () {
    fetchResearches();
    fetchPeerExperts();

    // Optional: Refresh data periodically
    setInterval(() => {
        fetchResearches();
        fetchPeerExperts();
    }, 1000);
});

//** researches **?//

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
                detailsButton.addEventListener("click", () => openResearchModal(research));

                item.appendChild(title);
                item.appendChild(detailsButton);

                approvalContainer.appendChild(item);
            });
        })
        .catch(error => {
            console.error("Error fetching researches:", error);
        });
}

function openResearchModal(research) {
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
        const li = document.createElement("li");
        li.textContent = "Geen beperkingen";
        limitationsList.appendChild(li);
    }

    const approveButton = document.getElementById("modalApproveButton");
    const rejectButton = document.getElementById("modalRejectButton");

    approveButton.onclick = () => approveResearch(research.research_id);
    rejectButton.onclick = () => rejectResearch(research.research_id);

    const modalElement = document.getElementById("researchModal");
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

function approveResearch(research_id) {
    fetch(`/api/researches/${research_id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
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
        headers: {
            "Content-Type": "application/json",
        },
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

//** ---- peer experts ---- **//

function fetchPeerExperts() {
    fetch("/api/peers?sort_by=peer_expert_id&sort_order=asc")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("newPeerExpertsContainer");
            const message = document.getElementById("noNewPeerExpertsMessage");

            container.innerHTML = "";

            const newPeerExperts = data.peer_experts.filter(peer => peer.peer_expert_status_id === 1);

            if (newPeerExperts.length === 0) {
                message.classList.remove("d-none");
                return;
            }

            message.classList.add("d-none");

            newPeerExperts.forEach(peer => {
                const item = document.createElement("div");
                item.classList.add("border", "rounded-3", "p-3", "d-flex", "justify-content-between", "align-items-center");

                const info = document.createElement("p");
                info.classList.add("mb-0");
                info.textContent = `${peer.user.first_name} ${peer.user.last_name} (${peer.postal_code})`;

                const detailsButton = document.createElement("button");
                detailsButton.textContent = "Details";
                detailsButton.classList.add("btn", "btn-info", "me-2");
                detailsButton.addEventListener("click", () => openPeerExpertModal(peer.peer_expert_id));

                item.appendChild(info);
                item.appendChild(detailsButton);

                container.appendChild(item);
            });
        })
        .catch(error => {
            console.error("Error fetching peer experts:", error);
        });
}

function openPeerExpertModal(peer_id) {
    fetch(`/api/peers/${peer_id}`)
        .then(response => response.json())
        .then(peer => {
            document.getElementById("peerExpertModalTitle").textContent = `${peer.user.first_name} ${peer.user.last_name}`;
            document.getElementById("peerFirstName").textContent = peer.user.first_name;
            document.getElementById("peerLastName").textContent = peer.user.last_name;
            document.getElementById("peerEmail").textContent = peer.user.email;
            document.getElementById("peerPhoneNumber").textContent = peer.user.phone_number || "Geen telefoonnummer";
            document.getElementById("peerPostalCode").textContent = peer.postal_code;
            document.getElementById("peerGender").textContent = peer.gender;
            document.getElementById("peerBirthDate").textContent = formatDate(peer.birth_date);
            document.getElementById("peerToolsUsed").textContent = peer.tools_used || "Geen hulpmiddelen";
            document.getElementById("peerShortBio").textContent = peer.short_bio || "Geen bio";
            document.getElementById("peerSpecialNotes").textContent = peer.special_notes || "Geen notities";
            document.getElementById("peerAvailabilityNotes").textContent = peer.availability_notes || "Geen info";

            const limitationsList = document.getElementById("peerLimitationsList");
            limitationsList.innerHTML = "";
            if (peer.limitations && peer.limitations.length > 0) {
                peer.limitations.forEach(limit => {
                    const li = document.createElement("li");
                    li.textContent = limit.limitation || limit.limitation_id;
                    limitationsList.appendChild(li);
                });
            } else {
                limitationsList.innerHTML = "<li>Geen beperkingen</li>";
            }

            const researchTypesList = document.getElementById("peerResearchTypesList");
            researchTypesList.innerHTML = "";
            if (peer.research_types && peer.research_types.length > 0) {
                peer.research_types.forEach(type => {
                    const li = document.createElement("li");
                    li.textContent = type.research_type || type.research_type_id;
                    researchTypesList.appendChild(li);
                });
            } else {
                researchTypesList.innerHTML = "<li>Geen onderzoek types</li>";
            }

            const approveBtn = document.getElementById("modalApprovePeerButton");
            const rejectBtn = document.getElementById("modalRejectPeerButton");

            approveBtn.onclick = () => approvePeerExpert(peer.peer_expert_id);
            rejectBtn.onclick = () => rejectPeerExpert(peer.peer_expert_id);

            const modalElement = document.getElementById("peerExpertModal");
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        })
        .catch(error => {
            console.error("Error fetching peer expert details:", error);
        });
}

function approvePeerExpert(peer_id) {
    fetch(`/api/peers/${peer_id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ peer_expert_status_id: 2 })
    })
        .then(response => {
            if (!response.ok) throw new Error("Goedkeuren niet gelukt.");
            return response.json();
        })
        .then(() => {
            showAlert("Ervaringsdeskundige is goedgekeurd.", "success");
            bootstrap.Modal.getInstance(document.getElementById("peerExpertModal")).hide();
            fetchPeerExperts();
        })
        .catch(error => {
            console.error(error);
            showAlert("Goedkeuren mislukt.", "danger");
        });
}

function rejectPeerExpert(peer_id) {
    fetch(`/api/peers/${peer_id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ peer_expert_status_id: 3 })
    })
        .then(response => {
            if (!response.ok) throw new Error("Afkeuren niet gelukt.");
            return response.json();
        })
        .then(() => {
            showAlert("Ervaringsdeskundige is afgekeurd.", "success");
            bootstrap.Modal.getInstance(document.getElementById("peerExpertModal")).hide();
            fetchPeerExperts();
        })
        .catch(error => {
            console.error(error);
            showAlert("Afkeuren mislukt.", "danger");
        });
}


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

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('nl-NL', { year: 'numeric', month: 'long', day: 'numeric' });
}