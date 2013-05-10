$(function () {
    $('.popup-gallery').magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0, 1]
        },
        image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
            titleSrc: function (item) {
                return '<p data-audio="' + item.el.attr('data-audio') + '">' + item.el.attr('title') + '</p>'
            },
        markup: '<div class="mfp-figure">'+
                    '<div class="mfp-close"></div>'+
                    '<div class="mfp-img-holder">'+
                        '<div class="mfp-img"></div>'+
                        '<div class="mfp-controls">'+
                            '<i class="icon-play audio"></i><i class="icon-pause audio" style="display:none"></i>'+
                        '</div>'+
                    '</div>'+
                    '<div class="mfp-bottom-bar">'+
                        '<div class="mfp-title"></div>'+
                        '<div class="mfp-counter"></div>'+
                    '</div>'+
                '</div>'
        },
        closeBtnInside: true,
        callbacks: {
            updateStatus: function () {
                $.scPlayer.stopAll();
                var audio = $('.mfp-title p').data('audio');
                var controls = $('.mfp-controls');
                if(audio != "None") {
                    var player = $('.player');
                    player.empty();
                    player.append('<a href="http://api.soundcloud.com/tracks/' + audio + '" class="sc-player">Player</a>');
                    $('.sc-player').scPlayer();
                    
                    controls.show();
                    $('i.icon-play', controls).show();
                    $('i.icon-pause', controls).hide();
                    $('.audio', controls).click(function () {
                        $('.audio', controls).toggle();
                        $('.sc-play').click();
                    });
                } else {
                    controls.hide();
                }
            },
            close: function () {
                $.scPlayer.stopAll();
            }
        }
    });
});
