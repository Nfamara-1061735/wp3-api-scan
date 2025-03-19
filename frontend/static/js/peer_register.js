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

    function checkDate() {
        const birthDateInput = document.querySelector('input[name="birth_date"]');
        const birthDate = new Date(birthDateInput.value);
        const today = new Date();
        const age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        const dayDiff = today.getDate() - birthDate.getDate();

        // Zet checkbox automatisch aan als jonger dan 18
        if (age < 18 || (age === 18 && (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)))) {
            supervisorCheckbox.checked = true;
            supervisorCheckbox.disabled = true
            console.log('young')
        } else {
            console.log('old')
            supervisorCheckbox.checked = false;
            supervisorCheckbox.disabled = false
        }

        toggleSupervisorField();
    }

    // Leeftijdscontrole
    const birthDateInput = document.querySelector('input[name="birth_date"]');
    birthDateInput.addEventListener("change", checkDate);

    // Luister naar veranderingen op de checkbox
    supervisorCheckbox.addEventListener('change', toggleSupervisorField);

    // Bij laden direct controleren
    checkDate();
    toggleSupervisorField();
});

const form = document.querySelector(".registration-form");

form.addEventListener("submit", function(e) {
    e.preventDefault(); // Voorkom standaard verzenden van het formulier

    let valid = true;

    // Functie om foutmeldingen te tonen/verbergen
    function showError(inputId, errorMessage) {
        const errorElement = document.getElementById(inputId + "_error");
        const inputElement = document.getElementById(inputId);

        if (errorMessage) {
            inputElement.classList.add('invalid');
            errorElement.textContent = errorMessage;
            errorElement.style.display = 'block';
            valid = false;
        } else {
            inputElement.classList.remove('invalid');
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    }
