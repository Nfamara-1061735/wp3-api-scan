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
                approvalContainer.innerHTML = "<p class='text muted'>Geen nieuwe onderzoeken om weer te geven.</p>";
                return;
            }

            newResearches.forEach(research => {
                const item = document.createElement("div");
                item.classList.add("border", "rounded-3", "p-3");

                const title = document.createElement("p");
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


}

