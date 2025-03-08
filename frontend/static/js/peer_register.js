document.addEventListener("DOMContentLoaded", function() {

    // Leeftijdscontrole (je bestaande functie blijft behouden)
    const birthDateInput = document.querySelector('input[name="birth_date"]');
    if (birthDateInput) {
        birthDateInput.addEventListener("change", function() {
            const birthDate = new Date(birthDateInput.value);
            const today = new Date();
            const age = today.getFullYear() - birthDate.getFullYear();
            const monthDiff = today.getMonth() - birthDate.getMonth();
            const dayDiff = today.getDate() - birthDate.getDate();

            // Zet checkbox automatisch aan als jonger dan 18
            if (age < 18 || (age === 18 && (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)))) {
                supervisorCheckbox.checked = true;
                toggleSupervisorField();
            }
        });
    }

    // Initialiseer weergave bij pagina laden
    toggleSupervisorField();
});
