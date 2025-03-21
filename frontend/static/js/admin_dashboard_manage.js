function formatDate(dateString) {
    // Create a date from the provided date string
    const date = new Date(dateString);

    // Options for formatting the date
    const options = {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    };

    // Convert the date to the desired format
    return date.toLocaleDateString('nl-NL', options);
}

$(document).ready(function () {
    // Add event listener to the 'Details' button
    $('#peerTable').on('click', '.btn-primary', function () {
        const peerExpertId = $(this).closest('tr').find('td').first().text();
        openPeerDetailsModal(peerExpertId);
    });

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

    // Usage example:
    loadPreferences('/api/contact_preferences', 'contact_preference_id', 'type', '#contactPreference');
    loadPreferences('/api/peers/status', 'peer_expert_status_id', 'status', '#peerStatus');
    loadPreferencesCheckboxes('/api/researches/types', 'research', 'research_type_id', 'type', '#researchType');
    loadPreferencesCheckboxes('/api/limitations', 'limitation', 'limitation_id', 'limitation', '#disabilities', 'limitation_category');

    // Function to open the modal and fetch peer details
    function openPeerDetailsModal(peerExpertId) {
        $.ajax({
            url: `/api/peers/${peerExpertId}`,
            method: 'GET',
            success: function (response) {

                $('#peerDetailsModal input[type="checkbox"]').prop('checked', false)

                // Fill the modal form with the data
                $('#peerExpertId').val(response.peer_expert_id);
                $('#firstName').val(response.user.first_name);
                $('#lastName').val(response.user.last_name);
                $('#postalCode').val(response.postal_code);
                $('#gender').val(response.gender);
                console.log();

                // Parse date
                const birthDate = new Date(response.birth_date)
                const birthDateDay = ("0" + birthDate.getDate()).slice(-2);
                const birthDateMonth = ("0" + (birthDate.getMonth() + 1)).slice(-2);
                const birthDateParsed = birthDate.getFullYear() + "-" + (birthDateMonth) + "-" + (birthDateDay);
                $('#birthDate').val(birthDateParsed);
                $('#email').val(response.user.email);
                $('#phoneNumber').val(response.user.phone_number);
                $('#toolsUsed').val(response.tools_used);
                $('#shortBio').val(response.short_bio);
                $('#specialNotes').val(response.special_notes);
                $('#availabilityNotes').val(response.availability_notes);

                // Set supervisor/guardian fields if applicable
                $('#hasSupervisor').prop('checked', response.has_supervisor);
                $('#supervisorOrGuardianName').val(response.supervisor_or_guardian_name);
                $('#supervisorOrGuardianEmail').val(response.supervisor_or_guardian_email);
                $('#supervisorOrGuardianPhone').val(response.supervisor_or_guardian_phone);

                checkDate(); // Update hasSupervisor checkbox

                // Set the status and contact preference dropdowns (if data is available)
                if (response.peer_expert_status_id) {
                    $('#peerStatus').val(response.peer_expert_status_id);
                }
                if (response.contact_preference_id) {
                    $('#contactPreference').val(response.contact_preference_id);
                }

                response.limitations.forEach(function (limitation) {
                    $('#limitation-preference-' + limitation.limitation_id).prop('checked', true);
                });

                response.research_types.forEach(function (type) {
                    $('#research-preference-' + type.research_type_id).prop('checked', true);
                });

                // Set accepted terms checkbox
                $('#acceptedTerms').prop('checked', response.accepted_terms);

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
    }

    // Add event listener to update URL when tab is clicked
    $('.nav-link').on('click', function () {
        var tabId = $(this).attr('id').replace('-tab', ''); // Extract tab ID from clicked tab
        // Update the URL with the selected tab
        var url = new URL(window.location);
        url.searchParams.set('tab', tabId);
        history.pushState(null, '', url); // Update the URL without reloading
    });

    let currentPage = 0;
    let maxPages = 0;
    let peerShowClosed = false;

    // Function to fetch and populate the table
    function fetchData(sortBy = 'peer_expert_id', sortOrder = 'asc', page = 1) {
        let queryParams = {
            sort_by: sortBy,
            sort_order: sortOrder,
            max_entries: 30,
            page: page
        };

        // Add the show_all parameter if the toggle is enabled
        if (peerShowClosed) {
            queryParams.show_all = true;
        }

        $.ajax({
            url: '/api/peers',
            method: 'GET',
            data: queryParams,
            success: function (response) {
                // Clear the table body
                $('#peerTable tbody').empty();

                $('#currentPage').val(response.pagination.current_page);

                currentPage = response.pagination.current_page;
                maxPages = response.pagination.total_pages;

                if (response.pagination.current_page <= 1) {
                    // Disable previous page buttons
                    $('#firstPage').prop("disabled", true);
                    $('#previousPage').prop("disabled", true);
                } else {
                    // Enable previous page buttons
                    $('#firstPage').prop("disabled", false);
                    $('#previousPage').prop("disabled", false);

                }

                if (response.pagination.current_page >= response.pagination.total_pages) {
                    // Disable next page buttons
                    $('#lastPage').prop("disabled", true);
                    $('#nextPage').prop("disabled", true);
                } else {
                    // Enable next page buttons
                    $('#lastPage').prop("disabled", false);
                    $('#nextPage').prop("disabled", false);
                }

                // Iterate over the response data and create rows dynamically
                response.peer_experts.forEach(function (peerExpert) {
                    var row = $('<tr>');
                    row.append('<td>' + peerExpert.peer_expert_id + '</td>');
                    row.append('<td>' + peerExpert.user.first_name + '</td>');
                    row.append('<td>' + peerExpert.user.last_name + '</td>');
                    row.append('<td>' + peerExpert.postal_code + '</td>');
                    row.append('<td>' + peerExpert.gender + '</td>');
                    row.append('<td>' + formatDate(peerExpert.birth_date) + '</td>');
                    row.append('<td><button class="btn btn-primary">Details</button></td>');
                    $('#peerTable tbody').append(row);
                });
            },
            error: function (error) {
                console.error("Error fetching data:", error);
                $('#alertContainer').removeClass('d-none').text('Failed to load data')
            }
        });
    }

    // Call fetchData to initially populate the table
    fetchData();

    let sortName = 'peer_expert_id';
    let sortOrder = 'asc';

    $('#peerShowClosed').prop("checked", false).on('change', function () {
        peerShowClosed = $(this).prop('checked');
        fetchData(sortName, sortOrder, currentPage);
    });

    // Add event listeners to the page buttons
    $('#firstPage').on('click', function () {
        if (currentPage > 1) {
            fetchData(sortName, sortOrder, 1);  // Fetch the first page
        }
    });

    $('#previousPage').on('click', function () {
        if (currentPage > 1) {
            fetchData(sortName, sortOrder, currentPage - 1);  // Fetch the previous page
        }
    });

    $('#currentPage').on('input', function () {
        var currentPageParsed = parseInt($(this).val());
        if (currentPageParsed > 0) {
            if (currentPageParsed > maxPages) {
                currentPageParsed = maxPages
                $(this).val(maxPages)
            }
            currentPage = currentPageParsed
            fetchData(sortName, sortOrder, currentPage);
        } else {
            $(this).val(currentPage)
        }
    });

    $('#nextPage').on('click', function () {
        if (currentPage < maxPages) {
            fetchData(sortName, sortOrder, currentPage + 1);  // Fetch the next page
        }
    });

    $('#lastPage').on('click', function () {
        if (currentPage < maxPages) {
            fetchData(sortName, sortOrder, maxPages);  // Fetch the last page
        }
    });

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

    $('#deletePeer').on('click', function (event) {
        const peerExpertId = $('#peerExpertId').val();  // Get the peer expert ID

        // Confirm deletion (optional, you can remove this if not needed)
        const confirmDelete = confirm('Weet je zeker dat je deze ervaringsdeskundige wilt verwijderen?');
        if (!confirmDelete) {
            return;
        }

        // Make the DELETE request to remove the peer details
        $.ajax({
            url: `/api/peers/${peerExpertId}`,
            method: 'DELETE',
            success: function (response) {
                $('#peerDetailsModal').modal('hide');
                fetchData(sortName, sortOrder, currentPage);  // Reload the data after deletion
            },
            error: function (error) {
                console.error("Error deleting peer expert details:", error);
                $('#modalAlertContainer').removeClass('d-none').removeClass('alert-info').addClass('alert-danger').text('Kon ervaringsdeskundige niet verwijderen').show();
            }
        });
    });

    // Iterate over each <th> in the table header
    $('#peerTable thead th').each(function () {
        // Get the sorting name from the custom attribute 'data-sort-name'
        var sortName = $(this).attr('data-sort');

        if (sortName) {
            // Create a new button element with the sorting name
            var button = $('<button class="p-0 btn btn-link"></button>').text($(this).text());

            // Set the custom sorting name as a data attribute on the button
            button.attr('data-sort', sortName);

            // Append the button to the <th> cell
            $(this).html(button);
        }
    });

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

    // Handle the click event on any button in the table header
    $('#peerTable thead').on('click', 'button', function () {
        // Remove the 'active' class from all buttons
        $('#peerTable thead button').not(this).find('i').remove();

        // Get the sorting name from the clicked button's custom attribute
        sortName = $(this).attr('data-sort');

        // Check if the clicked button already has an icon
        const currentIcon = $(this).find('i');
        if (currentIcon.length > 0) {
            if (currentIcon.hasClass('bi-sort-down')) {
                // If it has "bi-sort-down", change it to "bi-sort-up"
                currentIcon.removeClass('bi-sort-down').addClass('bi-sort-up');
            } else {
                currentIcon.removeClass('bi-sort-up').addClass('bi-sort-down');
            }
        } else {
            // Otherwise, append "bi-sort-down" icon
            var icon = $('<i class="ms-1 bi bi-sort-up"></i>');
            $(this).append(icon);
        }

        sortOrder = $(this).find('i').hasClass('bi-sort-down') ? 'desc' : 'asc';

        // Fetch data with updated sorting
        fetchData(sortName, sortOrder);
    });
});
