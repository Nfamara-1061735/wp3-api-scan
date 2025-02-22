$(document).ready(function () {
    $('#themeToggle').on('click', function () {
        const body = $('body')
        const currentTheme = body.attr('data-bs-theme');

        if (currentTheme === 'light') {
            body.attr('data-bs-theme', 'dark');
            $('#themeToggle').text('🌞').prop('title', 'Selecteer lichte thema');
        } else {
            body.attr('data-bs-theme', 'light');
            $('#themeToggle').text('🌙').prop('title', 'Selecteer donkere thema');
        }
    });
});