$(function () {
    $('.compressed').click(function() {
        $('.extra').show();
        $('.captchafield').removeClass('span3')
        $('.captchafield').addClass('span6')
    });
});