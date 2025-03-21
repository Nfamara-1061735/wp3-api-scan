function formatDate(dateString) {
    // Create a date from the provided date string
    const date = new Date(dateString);

    // Options for formatting the date
    const options = {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    };

    // Convert the date to the desired format
    const formattedDateString = date.toLocaleDateString('nl-NL', options) + ` ${String(date.getHours())}:${String(date.getMinutes()).padStart(2, '0')}`;

    // Capitalize the first letter and return it
    return formattedDateString.charAt(0).toUpperCase() + formattedDateString.slice(1);
}

let map = null

function initializeMap() {
    if (map != null)
        return;

    map = L.map('map');

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

function getRandomRange(min, max) {
    return Math.random() * (max - min) + min;
}

function getRandomCoordinates(location) {
    // Randomly generate coordinates within the bounds of the Netherlands
    const latMin = 50.75, latMax = 53.75;
    const lonMin = 3.25, lonMax = 7.25;

    // Create a random value within the latitude and longitude range
    const latitude = getRandomRange(latMin, latMax)
    const longitude = getRandomRange(lonMin, lonMax)

    return [latitude, longitude];
}

function updateOpenCards() {
    // Fetch the research data
    $.ajax({
        url: '/api/researches/registration-state?state=unregistered',
        type: 'GET',
        success: function (data) {
            $('#open-card-count').text(data.length);
            $('#open-card-container').empty()

            data.forEach(function (research) {
                // Create a new card for each research item
                var cardClone = $('<div class="card card-body col-2 d-flex flex-column"></div>');
                var cardTitle = $('<h5 class="card-title"></h5>').text(research.title);
                var cardDescription = $('<p class="card-text"></p>').text(research.description);
                var cardButton = $('<button class="btn btn-primary mt-auto">Meer informatie</button>')

                // Append the title and description to the card
                cardClone.append(cardTitle, $('<hr>'), cardDescription, cardButton);

                // Append the card to the container
                $('#open-card-container').append(cardClone);

                // TEMP: Add random lat and long
                research.latLon = getRandomCoordinates()

                // Attach the data to the button
                cardButton.data('research', research);

                // Add click event listener to the button
                cardButton.on('click', handleCardButtonClick);
            });
        },
        error: function (x) {
            console.log(x)
            // Show error message for any server issues
            $('#error-message').text('Er is een fout opgetreden. Probeer het opnieuw.').show();
        }
    });
}

function updateRegisteredCards() {
    // Fetch the research data
    $.ajax({
        url: '/api/researches/registration-state?state=registered',
        type: 'GET',
        success: function (data) {
            $('#registered-card-count').text(data.length);
            $('#registered-card-container').empty()

            data.forEach(function (research) {
                // Create a new card for each research item
                var cardClone = $('<div class="card card-body col-2 d-flex flex-column"></div>');
                var cardTitle = $('<h5 class="card-title"></h5>').text(research.title);
                var cardDescription = $('<p class="card-text"></p>').text(research.description);
                var cardButton = $('<button class="btn btn-primary mt-auto">Meer informatie</button>')

                // Append the title and description to the card
                cardClone.append(cardTitle, $('<hr>'), cardDescription, cardButton);

                // Append the card to the container
                $('#registered-card-container').append(cardClone);

                // TEMP: Add random lat and long
                research.latLon = getRandomCoordinates()

                // Attach the data to the button
                cardButton.data('research', research);

                // Add click event listener to the button
                cardButton.on('click', handleCardButtonClick);
            });
        },
        error: function (x) {
            console.log(x)
            // Show error message for any server issues
            $('#error-message').text('Er is een fout opgetreden. Probeer het opnieuw.').show();
        }
    });
}

function checkResearchRegistration(researchId) {
    $.ajax({
        url: '/api/peers/registrations?research_id=' + researchId,  // Assuming this endpoint returns a list of registrations for the current user
        type: 'GET',
        success: function (registrations) {
            // Check if there's a registration with the given research_id
            const registration = registrations.length > 0
            updateInterestedButton(registration, researchId)
        },
        error: function () {
            $('#error-message').text('Er is een fout opgetreden. Probeer het opnieuw.').show();
        }
    });
}

function updateInterestedButton(enabled, research_id) {
    // Update button text based on registration status
    const button = $('#interest-button')
    if (enabled) {
        button.text('Afschrijven')
            .removeClass('btn-primary')
            .addClass('btn-danger');
    } else {
        button.text('Geïnteresseerd')
            .removeClass('btn-danger')
            .addClass('btn-primary');
    }

    // Attach the click event listener to trigger the desired function with the current research_id
    button.off('click').on('click', function () {
        handleInterestButtonClick(research_id, enabled); // Call your function with the research_id
    });
}

function handleInterestButtonClick(research_id, sign_up) {
    if (sign_up) {
        // If the user is registered, send a DELETE request to unregister
        $.ajax({
            url: '/api/peers/registrations?research_id=' + research_id,  // Assuming this endpoint returns a list of registrations for the current user
            type: 'GET',
            success: function (registrations) {
                // Check if there's a registration with the given research_id
                registrations.forEach(function (registration) {
                    $.ajax({
                        url: '/api/peers/registrations/' + registration.peer_expert_registration_id,
                        type: 'DELETE',
                        success: function (response) {
                            updateInterestedButton(false, research_id)
                            updateOpenCards()
                        },
                        error: function (error) {
                            console.log(error)
                            console.log(error.responseText)
                            $('#error-message').text('Er is een fout opgetreden. Probeer het opnieuw.').show();
                        }
                    });
                });
            },
            error: function () {
                console.log(error.responseText)
                $('#error-message').text('Er is een fout opgetreden. Probeer het opnieuw.').show();
            }
        });
    } else {
        $.ajax({
            url: '/api/peers/registrations',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({research_id: research_id}),
            success: function (response) {
                updateInterestedButton(true, research_id)
                updateOpenCards()
            },
            error: function (error) {
                console.log(error.responseText)
                $('#error-message').text('Er is een fout opgetreden. Probeer het opnieuw.').show();
            }
        });
    }
}

function handleCardButtonClick(research_button) {
    const research = $(this).data('research');

    $('#researchModalTitle').text(research.title);
    $('#researchModalBody').text(research.description);

    $('#researchStartDate').text(formatDate(research.start_date));
    $('#researchEndDate').text(formatDate(research.end_date));

    $('#researchLocation').text(research.location);

    var ageRange = research.target_min_age + ' - ' + research.target_max_age;
    $('#researchAgeRange').text(ageRange);

    if (research.has_reward) {
        $('#researchReward').text(research.reward || 'Beloningsdetails niet beschikbaar');
    } else {
        $('#researchReward').text('Geen beloning beschikbaar');
    }

    var limitationsList = $('#researchLimitations');
    limitationsList.empty();
    if (research.limitations.length > 0) {
        research.limitations.forEach(function (limitation) {
            limitationsList.append('<li>' + limitation.limitation + '</li>');
        });
    } else {
        limitationsList.append('<li>Geen specifieke beperkingen</li>');
    }

    checkResearchRegistration(research.research_id)

    initializeMap();

    map.setView(research.latLon, 13);

    $('#researchModal').modal('show');
}

$(document).ready(function () {
    updateOpenCards()
    setInterval(updateOpenCards, 10000);
});

$(document).ready(function () {
    updateRegisteredCards()
    setInterval(updateRegisteredCards, 10000);
});

$('#researchModal').on('show.bs.modal', function () {
    setTimeout(function () {
        map.invalidateSize();
    }, 500);
});