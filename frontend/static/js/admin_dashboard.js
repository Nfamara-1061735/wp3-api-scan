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

function addElement() {

}