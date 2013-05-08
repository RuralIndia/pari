$(function(){
    $(".media-popup").on("show", function () {
        var youtube_url = "http://www.youtube.com/embed/" + $(this).data('video') + "?autoplay=1";
        $('.video-container', this).html('<iframe src="' + youtube_url + '" frameborder="0" allowfullscreen></iframe>');
    });

    $(".media-popup").on('hidden', function () {
        $('.video-container', this).html('');
    });
});