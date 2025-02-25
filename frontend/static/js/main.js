$(document).ready(function () {

    // Function to set a cookie with a specific name, value, and expiration in days.
    // Defaults to 365.2422 days (~1 year)
    function setCookie(name, value, days = 365.242199) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        let expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/";
    }

    // Function to get the value of the cookie by name
    function getCookie(name) {
        let match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }

    // Functions to set themes
    function setDarkMode() {
        $('body').attr('data-bs-theme', 'dark');
        $('#themeToggle').text('🌞').prop('title', 'Selecteer lichte thema');
        setCookie('theme', 'dark'); // Store theme in cookie for default days
    }

    function setLightMode() {
        $('body').attr('data-bs-theme', 'light');
        $('#themeToggle').text('🌙').prop('title', 'Selecteer donkere thema');
        setCookie('theme', 'light'); // Store theme in cookie for default days
    }

    // Check if the theme is stored in a cookie and set the appropriate theme
    const savedTheme = getCookie('theme');
    if (savedTheme) {
        if (savedTheme === 'dark') {
            setDarkMode();
        } else {
            setLightMode();
        }
    } else {
        // Default to light theme if no cookie is found
        setLightMode();
    }

    // Called when theme toggle button is clicked
    $('#themeToggle').on('click', function () {
        const body = $('body')
        const currentTheme = body.attr('data-bs-theme');

        // Set theme depending on current theme
        if (currentTheme === 'light') {
            body.attr('data-bs-theme', 'dark');
            setDarkMode();
        } else {
            body.attr('data-bs-theme', 'light');
            setLightMode();
        }
    });
});