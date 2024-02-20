$(document).ready(function () {
    $('#menu-icon').click(function () {
        $('.navbar-links').toggleClass('show-links');

        if ($(window).width() <= 900) {
            $('.navbar-links .profile-options').remove();

            // Copy profile options to bar icon dropdown
            var profileOptions = $('.profile-dropdown .dropdown-content').html();

            $('.navbar-links').append('<div class="profile-options">' + profileOptions + '</div>');
        } else {
            $('.navbar-links .profile-options').remove();
        }
    });

    $('#profile-image').click(function () {
        $('.profile-dropdown').toggleClass('active');
    });

    $(document).click(function (event) {
        if (!$(event.target).closest('.profile-dropdown').length) {
            $('.profile-dropdown').removeClass('active');
        }
    });
});

$(window).resize(function () {
    if ($(window).width() > 900) {
        $('.navbar-links').removeClass('show-links');
        $('.navbar-links .profile-options').remove();
    }
});
