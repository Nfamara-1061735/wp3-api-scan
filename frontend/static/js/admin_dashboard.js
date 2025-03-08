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
function fetchItems() {
    fetch("/admin/dashboard")
        .then(response => response.json())
        .then(data => createColumns(data))
        .then(error => console.error("Error fetching data:", error))
}

function createColumns(data) {
    const container = document.getElementById("researchContainer");

    data.forEach(item => {
        let div = document.createElement("div");
        div.classList.add("research-card");

        switch(data.json("research-type-id")){

        }
        container.appendChild(div);
    });
}

function testWrite(data) {
    document.write(data)
}