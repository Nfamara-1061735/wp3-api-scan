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

    // Valideer postcode
    const postalCode = document.getElementById('postal_code');
    const postalPattern = /^[0-9]{4}[A-Za-z]{2}$/;
    showError('postal_code', postalPattern.test(postalCode.value) ? '' : 'Vul een geldige postcode in (bijvoorbeeld 1234AB).');

    // Valideer geslacht
    const gender = document.getElementById('gender');
    showError('gender', gender.value ? '' : 'Selecteer je geslacht.');

    // Valideer geboortedatum
    const birthDate = document.getElementById('birth_date');
    showError('birth_date', birthDate.value ? '' : 'Vul je geboortedatum in.');

    // Valideer korte bio
    const shortBio = document.getElementById('short_bio');
    showError('short_bio', shortBio.value.trim() ? '' : 'Geef een korte bio.');

    // Valideer beschikbaarheid
    const availabilityNotes = document.getElementById('availability_notes');
    showError('availability_notes', availabilityNotes.value.trim() ? '' : 'Vul je beschikbaarheid in.');

    // Valideer contactvoorkeur
    const contactPreference = document.getElementById('contact_preference_id');
    showError('contact_preference_id', contactPreference.value ? '' : 'Geef je contactvoorkeur op.');

    // Valideer gebruikers ID
    const userId = document.getElementById('user_id');
    showError('user_id', userId.value ? '' : 'Kies een gebruikersid.');

    // Als alles correct is ingevuld versturen we het formulier
    if (valid) {
        form.submit();
    }
});