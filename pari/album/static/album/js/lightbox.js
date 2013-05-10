$(function() {
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
                if(item.el.attr('data-audio')!='None') {
                    sc_player_element = '<div class="post"><a href="https://soundcloud.com/'+item.el.attr('data-audio')+'"  class="sc-player">Player</a></div>';
                }
                return item.el.attr('title')+sc_player_element
            }
        },
        closeBtnInside: true,
        callbacks: {
            updateStatus: function() {
                $('a.sc-player').scPlayer();
            }
        }
    });
});