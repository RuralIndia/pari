$(function () {
    $('.contactform').on('click.contactus', function() {
        $(this).addClass('expanded');
        $(this).off('click.contactus');
    });
});