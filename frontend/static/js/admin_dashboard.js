document.addEventListener("DOMContentLoaded", function () {
    fetchResearches();
});

function fetchResearches() {
    fetch("/api/researches")
        .then(response => response.json())
        .then(data => {
            const approvalContainer = document.getElementById("approvalContainer");
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
        const li = document.createElement("li");
        li.textContent = "Geen beperkingen";
        limitationsList.appendChild(li);
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
            alert("Onderzoek is goedgekeurd.");
            const modal = bootstrap.Modal.getInstance(document.getElementById("researchModal"));
            modal.hide();
            fetchResearches();
        })
        .catch(error => {
            console.error(error);
            alert("Goedkeuren mislukt.");
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
            alert("Onderzoek is afgekeurd.");
            const modal = bootstrap.Modal.getInstance(document.getElementById("researchModal"));
            modal.hide();
            fetchResearches();
        })
        .catch(error => {
            console.error(error);
            alert("Afkeuren mislukt.");
        });
}
