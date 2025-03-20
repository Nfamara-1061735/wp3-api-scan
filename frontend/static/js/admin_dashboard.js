document.addEventListener("DOMContentLoaded", function () {
    fetchResearches();

    setInterval(fetchResearches, 10000);
});

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
    limitationsList.innerHTML = ""; // Clear existing
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
    const modal = new bootstrap.Modal(modalElement)
    modal.show();
}

function approveResearch(research_id) {
    fetch(`/api/researches/${research_id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({status_id: 2})
    })
        .then(response => {
            if (!response.ok) throw new Error("Goedkeuren niet gelukt.");
            return response.json();
        })
        .then(() => {
            showAlert("Onderzoek is goedgekeurd.", "success");
            const modal = bootstrap.Modal.getInstance(document.getElementById("researchModal"));
            modal.hide();
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
        body: JSON.stringify({status_id: 3})
    })
        .then(response => {
            if (!response.ok) throw new Error("Afkeuren niet gelukt.");
            return response.json();
        })
        .then(() => {
            showAlert("Onderzoek is afgekeurd.", "success");
            const modal = bootstrap.Modal.getInstance(document.getElementById("researchModal"));
            modal.hide();
            fetchResearches();
        })
        .catch(error => {
            console.error(error);
            showAlert("Afkeuren mislukt.", "danger");
        });
}

function showAlert(message, type = "succes") {
    const alertContainer = document.getElementById("alertContainer");

    alertContainer.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Sluiten"></button>
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