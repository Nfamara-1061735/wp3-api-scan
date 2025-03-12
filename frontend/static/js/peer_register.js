document.addEventListener("DOMContentLoaded", function() {
    const supervisorCheckbox = document.getElementById('has_supervisor_checkbox');
    const supervisorGroup = document.getElementById('supervisor-name-group');

    // Functie om veld te tonen of verbergen
    function toggleSupervisorField() {
        if (supervisorCheckbox.checked) {
            supervisorGroup.style.display = "block";
        } else {
            supervisorGroup.style.display = "none";
        }
    }

    // Bij laden direct controleren
    toggleSupervisorField();

    // Luister naar veranderingen op de checkbox
    supervisorCheckbox.addEventListener('change', toggleSupervisorField);

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
