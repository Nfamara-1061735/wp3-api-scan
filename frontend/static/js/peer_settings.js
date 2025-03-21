function loadPreferences(url, idField, typeField, targetId) {
    $.ajax({
        url: url,
        method: 'GET',
        success: function (response) {
            response.forEach(function (contact_preference) {
                const preference = contact_preference[typeField][0].toUpperCase() + contact_preference[typeField].slice(1);
                const option = $('<option></option>').text(preference).prop('value', contact_preference[idField]);
                $(targetId).append(option);
            });
        },
        error: function (error) {
            console.error("Error fetching " + url + ":", error);
            $('#alertContainer').removeClass('d-none').text('Failed to load ' + url);
        }
    });
}

function loadPreferencesCheckboxes(url, name, idField, typeField, targetId, categoryField) {
    $.ajax({
        url: url,
        method: 'GET',
        success: function (response) {
            if (categoryField) {
                // Group preferences by category if categoryField is provided
                const groupedPreferences = {};

                response.forEach(function (contact_preference) {
                    const category = contact_preference[categoryField] || "Uncategorized"; // Default to "Uncategorized" if no category is available
                    if (!groupedPreferences[category]) {
                        groupedPreferences[category] = [];
                    }
                    groupedPreferences[category].push(contact_preference);
                });

                // Iterate through grouped preferences and create checkboxes
                for (const category in groupedPreferences) {
                    // Create a category label
                    const categoryLabel = $('<div class="category-label"></div>').text(category);
                    $(targetId).append(categoryLabel);

                    // Create checkboxes for each preference in the category
                    groupedPreferences[category].forEach(function (contact_preference) {
                        const preference = contact_preference[typeField][0].toUpperCase() + contact_preference[typeField].slice(1);
                        const checkbox = $('<div class="form-check"></div>');
                        const input = $('<input class="form-check-input" type="checkbox">')
                            .prop('value', contact_preference[idField])
                            .prop('id', name + '-preference-' + contact_preference[idField]);
                        const label = $('<label class="form-check-label"></label>')
                            .prop('for', name + '-preference-' + contact_preference[idField])
                            .text(preference);

                        checkbox.append(input).append(label);
                        $(targetId).append(checkbox);
                    });
                }
            } else {
                // If no categoryField is provided, simply create checkboxes without any category label
                response.forEach(function (contact_preference) {
                    const preference = contact_preference[typeField][0].toUpperCase() + contact_preference[typeField].slice(1);
                    const checkbox = $('<div class="form-check"></div>');
                    const input = $('<input class="form-check-input" type="checkbox">')
                        .prop('value', contact_preference[idField])
                        .prop('id', name + '-preference-' + contact_preference[idField]);
                    const label = $('<label class="form-check-label"></label>')
                        .prop('for', name + '-preference-' + contact_preference[idField])
                        .text(preference);

                    checkbox.append(input).append(label);
                    $(targetId).append(checkbox);
                });
            }
        },
        error: function (error) {
            console.error("Error fetching " + url + ":", error);
            $('#alertContainer').removeClass('d-none').text('Failed to load ' + url);
        }
    });
}

$(document).ready(function () {
    loadPreferences('/api/contact_preferences', 'contact_preference_id', 'type', '#contactPreference');
    loadPreferences('/api/peers/status', 'peer_expert_status_id', 'status', '#peerStatus');
    loadPreferencesCheckboxes('/api/researches/types', 'research', 'research_type_id', 'type', '#researchType');
    loadPreferencesCheckboxes('/api/limitations', 'limitation', 'limitation_id', 'limitation', '#disabilities', 'limitation_category');

    $.ajax({
        url: `/api/peers`,
        method: 'GET',
        success: function (response) {
            const peer_expert = response?.peer_experts?.[0] ?? null;

            if (peer_expert === undefined)
                return;

            $('#peerDetailsModal input[type="checkbox"]').prop('checked', false)

            // Fill the modal form with the data
            $('#peerExpertId').val(peer_expert.peer_expert_id);
            $('#firstName').val(peer_expert.user.first_name);
            $('#lastName').val(peer_expert.user.last_name);
            $('#postalCode').val(peer_expert.postal_code);
            $('#gender').val(peer_expert.gender);
            console.log();

            // Parse date
            const birthDate = new Date(peer_expert.birth_date)
            const birthDateDay = ("0" + birthDate.getDate()).slice(-2);
            const birthDateMonth = ("0" + (birthDate.getMonth() + 1)).slice(-2);
            const birthDateParsed = birthDate.getFullYear() + "-" + (birthDateMonth) + "-" + (birthDateDay);
            $('#birthDate').val(birthDateParsed);
            $('#email').val(peer_expert.user.email);
            $('#phoneNumber').val(peer_expert.user.phone_number);
            $('#toolsUsed').val(peer_expert.tools_used);
            $('#shortBio').val(peer_expert.short_bio);
            $('#specialNotes').val(peer_expert.special_notes);
            $('#availabilityNotes').val(peer_expert.availability_notes);

            // Set supervisor/guardian fields if applicable
            $('#hasSupervisor').prop('checked', peer_expert.has_supervisor);
            $('#supervisorOrGuardianName').val(peer_expert.supervisor_or_guardian_name);
            $('#supervisorOrGuardianEmail').val(peer_expert.supervisor_or_guardian_email);
            $('#supervisorOrGuardianPhone').val(peer_expert.supervisor_or_guardian_phone);

            checkDate(); // Update hasSupervisor checkbox

            // Set the status and contact preference dropdowns (if data is available)
            if (peer_expert.peer_expert_status_id) {
                $('#peerStatus').val(peer_expert.peer_expert_status_id);
            }
            if (peer_expert.contact_preference_id) {
                $('#contactPreference').val(peer_expert.contact_preference_id);
            }

            peer_expert.limitations.forEach(function (limitation) {
                $('#limitation-preference-' + limitation.limitation_id).prop('checked', true);
            });

            peer_expert.research_types.forEach(function (type) {
                $('#research-preference-' + type.research_type_id).prop('checked', true);
            });

            // Set accepted terms checkbox
            $('#acceptedTerms').prop('checked', peer_expert.accepted_terms);

            const form = $('peerDetailsForm')
            form.removeClass('was-validated')

            // Open the modal
            $('#modalAlertContainer').addClass('d-none')
            $('#peerDetailsModal').modal('show');
        },
        error: function (error) {
            console.error("Error fetching peer expert details:", error);
            $('#alertContainer').removeClass('d-none').text('Failed to load peer expert details');
        }
    });

    // Supervisor checkbox
    const supervisorCheckbox = $('#hasSupervisor');
    const supervisorGroup = $('#supervisorGroupCollapse');
    const supervisorInputs = $('#supervisorOrGuardianName, #supervisorOrGuardianEmail, #supervisorOrGuardianPhone, #supervisorAccordionButton');
    const birthDateInput = $('#birthDate');

    function toggleSupervisorField() {
        if (supervisorCheckbox.prop('checked')) {
            // Enable the fields and show the accordion
            supervisorInputs.prop('disabled', false);
            supervisorGroup.collapse('show'); // Ensure the accordion is expanded
        } else {
            // Disable the fields and collapse the accordion
            supervisorInputs.prop('disabled', true);
            supervisorGroup.collapse('hide'); // Collapse the accordion
        }
    }

    function checkDate() {
        const birthDate = new Date(birthDateInput.val());
        const today = new Date();
        const age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        const dayDiff = today.getDate() - birthDate.getDate();

        if (age < 18 || (age === 18 && (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)))) {
            supervisorCheckbox.prop('checked', true);
            supervisorCheckbox.prop('disabled', true);
        } else {
            supervisorCheckbox.prop('checked', false);
            supervisorCheckbox.prop('disabled', false);
        }

        toggleSupervisorField();
    }

    // Event handlers
    birthDateInput.on('change', checkDate);
    supervisorCheckbox.on('change', toggleSupervisorField);

    // Initial setup
    checkDate();
    toggleSupervisorField();

    // Function to handle save button click and update peer details
    $('#peerDetailsForm').on('submit', function (event) {
        // Reset form
        //$(this).addClass('was-validated');
        $('#peerDetailsForm .is-invalid').removeClass('is-invalid')

        if (!this[0].checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }

        // Gather form data
        const peerExpertId = $('#peerExpertId').val();
        const firstName = $('#firstName').val();
        const lastName = $('#lastName').val();
        const postalCode = $('#postalCode').val();
        const gender = $('#gender').val();
        const birthDate = $('#birthDate').val();
        const email = $('#email').val();
        const phoneNumber = $('#phoneNumber').val();
        const toolsUsed = $('#toolsUsed').val();
        const shortBio = $('#shortBio').val();
        const specialNotes = $('#specialNotes').val();
        const availabilityNotes = $('#availabilityNotes').val();
        const hasSupervisor = $('#hasSupervisor').prop('checked');
        const supervisorOrGuardianName = $('#supervisorOrGuardianName').val();
        const supervisorOrGuardianEmail = $('#supervisorOrGuardianEmail').val();
        const supervisorOrGuardianPhone = $('#supervisorOrGuardianPhone').val();
        const peerStatus = $('#peerStatus').val();
        const contactPreference = $('#contactPreference').val();
        const acceptedTerms = $('#acceptedTerms').prop('checked');

        // Gather limitations and research types
        const limitations = [];
        $('#disabilities input[type="checkbox"]').each(function () {
            if ($(this).prop('checked')) {
                limitations.push({limitation_id: $(this).val()});
            }
        });

        const researchTypes = [];
        $('#researchType input[type="checkbox"]').each(function () {
            if ($(this).prop('checked')) {
                researchTypes.push({research_type_id: $(this).val()});
            }
        });

        // Check if the password is changed
        const password = $('#password').val();
        const passwordVerify = $('#passwordVerify').val();
        let passwordField = null;
        if (password) {
            if (password === passwordVerify) {
                passwordField = password;  // Only include password if it was changed
            } else {
                $('#password').addClass('is-invalid');
                $('#passwordVerify').addClass('is-invalid');
                event.preventDefault()
                return;
            }
        }

        // Create the data object for the PATCH request
        const data = {
            peer_expert_id: peerExpertId,
            user: {
                first_name: firstName,
                last_name: lastName,
                email: email,
                phone_number: phoneNumber,
            },
            postal_code: postalCode,
            gender: gender,
            birth_date: birthDate,
            tools_used: toolsUsed,
            short_bio: shortBio,
            special_notes: specialNotes,
            availability_notes: availabilityNotes,
            has_supervisor: hasSupervisor,
            supervisor_or_guardian_name: supervisorOrGuardianName,
            supervisor_or_guardian_email: supervisorOrGuardianEmail,
            supervisor_or_guardian_phone: supervisorOrGuardianPhone,
            peer_expert_status_id: peerStatus,
            contact_preference_id: contactPreference,
            limitations: limitations,
            research_types: researchTypes,
            accepted_terms: acceptedTerms,
        };

        // Only add the password if it was changed
        if (passwordField) {
            data.user.password = passwordField;
        }

        // Make the PATCH request to update the peer details
        $.ajax({
            url: `/api/peers/${peerExpertId}`,
            method: 'PATCH',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (response) {
                $('#modalAlertContainer').removeClass('d-none').removeClass('alert-danger').addClass('alert-info').text('Ervaringsdeskundige details geüpdatet')[0].scrollIntoView();
                fetchData(sortName, sortOrder, currentPage); // Reload the data after update
            },
            error: function (error) {
                console.error("Error updating peer expert details:", error);
                $('#modalAlertContainer').removeClass('d-none').removeClass('alert-info').addClass('alert-danger').text('Kon ervaringsdeskundige details niet updaten')[0].scrollIntoView();
            }
        });
    });

    // Password
    $('#password').on('input', function () {
        if ($(this).val().length > 0) {
            $('#passwordConfirm').show();
        } else {
            $('#passwordConfirm').hide();
        }
    });

    $('#passwordConfirm').hide();
});