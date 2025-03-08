// document.addEventListener("DOMContentLoaded", function () {
//     const birthDateInput = document.querySelector('input[name="birth_date"]');
//     const supervisorCheckbox = document.querySelector('input[name="has_supervisor"]');
//
//     if (birthDateInput) {
//         birthDateInput.addEventListener("change", function () {
//             const birthDate = new Date(birthDateInput.value);
//             const today = new Date();
//             const age = today.getFullYear() - birthDate.getFullYear();
//             const monthDiff = today.getMonth() - birthDate.getMonth();
//             const dayDiff = today.getDate() - birthDate.getDate();
//
//             // Controleer of de gebruiker jonger dan 18 is
//             if (age < 18 || (age === 18 && (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)))) {
//                 supervisorCheckbox.checked = true;
//             } else {
//                 supervisorCheckbox.checked = false;
//             }
//         });
//     }
// });
