$(function () {
    $('.popup-gallery').magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
        },
        image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
            titleSrc: function (item) {
                sc_player_element = ""
                audio = item.el.attr('data-audio');
                if (audio != 'None') {
                    sc_player_element = ' <a href="#" class="audio"><i class="icon-volume-up"></i>  <i class="icon-volume-down" style="display: none"></i></a>';
                }
                return item.el.attr('title') + sc_player_element
            }
        },
        closeBtnInside: true,
        callbacks: {
            updateStatus: function () {
                $.scPlayer.stopAll();
                $('.player').empty()
                $('.player').append('<a href="http://api.soundcloud.com/tracks/' + audio + '" class="sc-player">Player</a>')
                $('.sc-player').scPlayer();
                $('.audio').click(function () {
                    $("i").toggle();
                    $('.sc-play').click();
                });
            },
            close: function () {
                $.scPlayer.stopAll();
            }
        }
    });
});
