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
    function toggleRewardDescription() {
        if ($('#researchHasReward').is(':checked')) {
            $('#researchRewardContainer').fadeIn();
        } else {
            $('#researchRewardContainer').fadeOut();
            $('#researchReward').val('');
        }
    }

    toggleRewardDescription();

    $('#researchHasReward').on('change', function () {
        toggleRewardDescription();
    });

    // Add event listener to the 'Details' button
    $('#peerTable').on('click', '.btn-primary', function () {
        const peerExpertId = $(this).closest('tr').find('td').first().text();
        openPeerDetailsModal(peerExpertId);
    });

    // Function to open the modal and fetch peer details
    function openPeerDetailsModal(peerExpertId) {
        $.ajax({
            url: `/api/peers/${peerExpertId}`,
            method: 'GET',
            success: function (response) {
                console.log(response);

                // Fill the modal form with the data
                $('#peerExpertId').val(response.peer_expert_id);
                $('#firstName').val(response.user.first_name);
                $('#lastName').val(response.user.last_name);
                $('#postalCode').val(response.postal_code);
                $('#gender').val(response.gender);
                $('#birthDate').val(response.birth_date);

                // Open the modal
                $('#peerDetailsModal').modal('show');
            },
            error: function (error) {
                console.error("Error fetching peer expert details:", error);
                $('#alertContainer').text('Failed to load peer expert details');
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

    // Function to fetch and populate the table
    function fetchData(sortBy = 'peer_expert_id', sortOrder = 'asc', page = 1) {
        $.ajax({
            url: '/api/peers',
            method: 'GET',
            data: {
                sort_by: sortBy,
                sort_order: sortOrder,
                max_entries: 30,
                page: page
            },
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
                    // row.append('<td class="text-truncate" title="' + peerExpert.tools_used + '">' + peerExpert.tools_used + '</td>');
                    // row.append('<td class="text-truncate" title="' + peerExpert.short_bio + '">' + peerExpert.short_bio + '</td>');
                    // row.append('<td class="text-truncate" title="' + peerExpert.special_notes + '">' + peerExpert.special_notes + '</td>');
                    // row.append('<td class="text-truncate" title="' + peerExpert.availability_notes + '">' + peerExpert.availability_notes + '</td>');
                    row.append('<td><button class="btn btn-primary">Details</button></td>'); // Example button
                    $('#peerTable tbody').append(row);
                });
            },
            error: function (error) {
                console.error("Error fetching data:", error);
                $('#alertContainer').text('Failed to load data')
            }
        });
    }

    // Call fetchData to initially populate the table
    fetchData();

    let sortName = 'peer_expert_id';
    let sortOrder = 'asc';

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

    // research functionality
    let researchCurrentPage = 1;
    let researchMaxPages = 1;
    let researchSortName = 'research_id';
    let researchSortOrder = 'asc';

    function fetchResearches(sortBy = 'research_id', sortOrder = 'asc', page = 1) {
        console.log(`Fetching researches... page ${page}`);
        $.ajax({
            url: '/api/researches-admin',
            method: 'GET',
            data: {
                sort_by: sortBy,
                sort_order: sortOrder,
                max_entries: 10,
                page: page
            },
            success: function (response) {
                console.log("Researches fetched:", response);

                $('#researchTable tbody').empty();
                $('#currentResearchPage').val(response.pagination.current_page);

                researchCurrentPage = response.pagination.current_page;
                researchMaxPages = response.pagination.total_pages;

                $('#firstResearchPage').prop('disabled', researchCurrentPage <= 1);
                $('#previousResearchPage').prop('disabled', researchCurrentPage <= 1);
                $('#nextResearchPage').prop('disabled', researchCurrentPage >= researchMaxPages);
                $('#lastResearchPage').prop('disabled', researchCurrentPage >= researchMaxPages);

                if (response.researches.length === 0) {
                    $('#researchTable tbody').append('<tr><td colspan="7">Geen onderzoeken gevonden.</td></tr>');
                    return;
                }

                response.researches.forEach(function (research) {
                    const statusBadge = getStatusBadge(research.status_id);
                    const row = $('<tr>').attr('data-research-id', research.research_id);
                    row.append(`<td class="text-center">${statusBadge}</td>`);
                    row.append(`<td>${research.title}</td>`);
                    row.append(`<td>${research.description || 'Geen beschrijving'}</td>`);
                    row.append(`<td>${research.start_date ? formatDate(research.start_date) : 'Onbekend'}</td>`);
                    row.append(`<td>${research.end_date ? formatDate(research.end_date) : 'Onbekend'}</td>`);
                    row.append(`<td>${research.location || 'Onbekend'}</td>`);
                    row.append('<td><button class="btn btn-info btn-sm">Details</button></td>');
                    $('#researchTable tbody').append(row);
                });
            },
            error: function () {
                $('#alertContainer').text('Fout bij laden van onderzoeken.');
            }
        });
    }

    $('#researchTable').on('click', '.btn-info', function () {
        const row = $(this).closest('tr');
        const researchId = row.data('research-id');
        openResearchDetailsModal(researchId);
    });

    function openResearchDetailsModal(researchId) {
        $.ajax({
            url: `/api/researches-admin/${researchId}`,
            method: 'GET',
            success: function (research) {
                $('#researchId').val(research.research_id);
                $('#researchTitle').val(research.title);
                $('#researchLocation').val(research.location);
                $('#researchDescription').val(research.description);
                $('#researchStartDate').val(research.start_date);
                $('#researchEndDate').val(research.end_date);
                $('#researchStatusId').val(research.status_id);
                $('#researchTypeId').val(research.research_type_id);
                $('#researchIsAvailable').prop('checked', research.is_available);
                $('#researchHasReward').prop('checked', research.has_reward);
                $('#researchReward').val(research.reward);
                $('#researchTargetMinAge').val(research.target_min_age);
                $('#researchTargetMaxAge').val(research.target_max_age);

                currentSelectedLimitations = research.limitations || [];
                updateSelectedLimitationsList();

                $('#researchDetailsModal').modal('show');
            },
            error: function () {
                $('#alertContainer').text('Fout bij laden van onderzoek details.');
            }
        });
    }

    function loadLimitations(selectedLimitations = []) {
        $.ajax({
            url: '/api/limitations/',
            method: 'GET',
            success: function (limitations) {
                const $select = $('#researchLimitations');
                $select.empty(); // Clear previous options


                const selectedIds = selectedLimitations.map(l => l.limitation_id);

                limitations.forEach(function (limitation) {
                    const isSelected = selectedIds.includes(limitation.limitation_id);
                    const option = $('<option>')
                        .val(limitation.limitation_id)
                        .text(limitation.limitation)
                        .prop('selected', isSelected);

                    $select.append(option);
                });
            },
            error: function () {
                console.error('Fout bij laden van beperkingen.');
                $('#alertContainer').text('Beperkingen ophalen is mislukt.');
            }
        });
    }

    $('#researchDetailsForm').on('submit', function (e) {
        e.preventDefault();

        const researchId = $('#researchId').val();
        const limitationIds = currentSelectedLimitations.map(l => l.limitation_id);

        const payload = {
            title: $('#researchTitle').val(),
            location: $('#researchLocation').val(),
            description: $('#researchDescription').val(),
            start_date: $('#researchStartDate').val(),
            end_date: $('#researchEndDate').val(),
            status_id: parseInt($('#researchStatusId').val()),
            research_type_id: parseInt($('#researchTypeId').val()),
            is_available: $('#researchIsAvailable').is(':checked'),
            has_reward: $('#researchHasReward').is(':checked'),
            reward: $('#researchReward').val(),
            target_min_age: parseInt($('#researchTargetMinAge').val()) || null,
            target_max_age: parseInt($('#researchTargetMaxAge').val()) || null,
            limitation_ids: limitationIds
        };

        $.ajax({
            url: `/api/researches-admin/${researchId}`,
            method: 'PATCH',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function () {
                $('#alertContainer').text('Onderzoek succesvol bijgewerkt.');
                $('#researchDetailsModal').modal('hide');
                fetchResearches();
            },
            error: function () {
                $('#alertContainer').text('Fout bij bijwerken van onderzoek.');
            }
        });
    });

    $('#deleteResearchBtn').on('click', function () {
        const researchId = $('#researchId').val();

        if (!confirm('Weet je zeker dat je dit onderzoek wilt verwijderen?')) return;

        $.ajax({
            url: `/api/researches-admin/${researchId}`,
            method: 'DELETE',
            success: function () {
                $('#alertContainer').text('Onderzoek succesvol verwijderd.');
                $('#researchDetailsModal').modal('hide');
                fetchResearches();
            },
            error: function () {
                $('#alertContainer').text('Fout bij verwijderen van onderzoek.');
            }
        });
    });


    $('#firstResearchPage').on('click', () => researchCurrentPage > 1 && fetchResearches(researchSortName, researchSortOrder, 1));
    $('#previousResearchPage').on('click', () => researchCurrentPage > 1 && fetchResearches(researchSortName, researchSortOrder, researchCurrentPage - 1));
    $('#nextResearchPage').on('click', () => researchCurrentPage < researchMaxPages && fetchResearches(researchSortName, researchSortOrder, researchCurrentPage + 1));
    $('#lastResearchPage').on('click', () => researchCurrentPage < researchMaxPages && fetchResearches(researchSortName, researchSortOrder, researchMaxPages));

    $('#currentResearchPage').on('input', function () {
        const page = parseInt($(this).val());
        if (page >= 1 && page <= researchMaxPages) {
            fetchResearches(researchSortName, researchSortOrder, page);
        } else {
            $(this).val(researchCurrentPage);
        }
    });

    $('#researchTable thead th').each(function () {
        const sort = $(this).attr('data-sort');
        if (sort) {
            const button = $('<button class="p-0 btn btn-link"></button>').text($(this).text());
            button.attr('data-sort', sort);
            $(this).html(button);
        }
    });

    $('#researchTable thead').on('click', 'button', function () {
        $('#researchTable thead button i').remove();
        researchSortName = $(this).attr('data-sort');
        const icon = $('<i class="ms-1 bi bi-sort-up"></i>');
        $(this).append(icon);
        researchSortOrder = $(this).find('i').hasClass('bi-sort-down') ? 'desc' : 'asc';
        fetchResearches(researchSortName, researchSortOrder);
    });


    $('#researches-tab').on('shown.bs.tab', function () {
        fetchResearches();
    });


    if ($('#researches').hasClass('show active')) {
        fetchResearches();
    }

    function getStatusBadge(statusId) {
        const baseStyle = 'width: 15px; height: 15px; display: inline-block;';
        switch (statusId) {
            case 1:
                return `<span class="badge bg-warning rounded-circle" style="${baseStyle}"></span>`;
            case 2:
                return `<span class="badge bg-success rounded-circle" style="${baseStyle}"></span>`;
            case 3:
                return `<span class="badge bg-danger rounded-circle" style="${baseStyle}"></span>`;
            case 4:
                return `<span class="badge bg-secondary rounded-circle" style="${baseStyle}"></span>`;
            default:
                return `<span class="badge bg-dark rounded-circle" style="${baseStyle}"></span>`;
        }
    }

    let currentSelectedLimitations = [];

    $('#openLimitationsModalBtn').on('click', function () {
        loadLimitationsModal();
        $('#limitationsModal').modal('show');
    });

    function loadLimitationsModal() {
        $.ajax({
            url: '/api/limitations/',
            method: 'GET',
            success: function (limitations) {
                const container = $('#limitationsCheckboxes');
                container.empty();

                const selectedIds = currentSelectedLimitations.map(l => l.limitation_id);

                limitations.forEach(function (limitation) {
                    const isChecked = selectedIds.includes(limitation.limitation_id);
                    const checkbox = `
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox"
                                   value="${limitation.limitation_id}"
                                   id="modal-limitation-${limitation.limitation_id}"
                                   ${isChecked ? 'checked' : ''}>
                            <label class="form-check-label" for="modal-limitation-${limitation.limitation_id}">
                                ${limitation.limitation}
                            </label>
                        </div>
                    `;
                    container.append(checkbox);
                });
            },
            error: function () {
                console.error('Fout bij laden van beperkingen.');
                $('#alertContainer').text('Beperkingen ophalen is mislukt.');
            }
        });
    }

    $('#saveLimitationsBtn').on('click', function () {
        const selectedIds = [];

        $('#limitationsCheckboxes input[type="checkbox"]:checked').each(function () {
            const limitationId = parseInt($(this).val());
            const limitationText = $(this).next('label').text();
            selectedIds.push({
                limitation_id: limitationId,
                limitation: limitationText
            });
        });

        currentSelectedLimitations = selectedIds;
        updateSelectedLimitationsList();
        $('#limitationsModal').modal('hide');
    });

    function updateSelectedLimitationsList() {
        const container = $('#selectedLimitationsList');
        container.empty();

        if (currentSelectedLimitations.length === 0) {
            container.html('<p class="text-muted">Geen beperkingen geselecteerd.</p>');
            return;
        }

        const list = $('<ul class="list-group list-group-flush"></ul>');

        currentSelectedLimitations.forEach(limitation => {
            const item = `<li class="list-group-item">${limitation.limitation}</li>`;
            list.append(item);
        });

        container.append(list);
    }
});

