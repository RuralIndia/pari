$(function () {
    $('.popup-gallery').magnificPopup({
        delegate: '.mfp-image',
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
                return '<div>'+
                            '<h4>'+ item.el.attr('data-photographer') + '</h4>' +
                            '<p class="image-date">' + item.el.attr('data-date') + '</p>' +
                            '<p class="image-location">' + item.el.attr('data-location') + '</p>' +
                            '<p class="image-caption" data-audio="' + item.el.attr('data-audio') + '">' + item.el.attr('title') + '</p>' +
                            '<div class="btn-toolbar">'+
                                '<div class="btn-group">'+
                                    '<a class="btn" href="' + item.el.attr('data-url') +'"><i class="icon-share"></i></a>'+
                                    '<a class="btn" href="' + item.el.attr('data-url') +'#comments"><i class="icon-comment-alt"></i></a>'+
                                    '<a class="btn btn-fullscreen" href="#"><i class="icon-fullscreen"></i></a>'+
                                '</div>'+
                            '</div>'+
                        '</div>'
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
                var audio = $('.mfp-title .image-caption').data('audio');
                var controls = $('.mfp-controls');

                $('.btn-fullscreen').on('click', function() {
                    $('.mfp-container').addClass('mfp-container-fullscreen');
                    return false;

                });

                $('.mfp-figure').on('click', function() {
                    $('.mfp-container').removeClass('mfp-container-fullscreen');

                });

                if(audio && audio != "") {
                    var player = $('.player');
                    player.empty();
                    player.append('<a href="http://api.soundcloud.com/tracks/' + audio + '" class="sc-player">Player</a>');
                    slideShow = $('.album-controls').is(':hidden');
                    $('.sc-player').scPlayer({
                        autoPlay: slideShow
                    });
                    controls.show();
                    $('.icon-play', controls).show();
                    $('.icon-pause', controls).hide();
                    $('.audio', controls).click(function () {
                        $('.sc-play').click();
                    });
                } else {
                    controls.hide();
                }
            },
            close: function () {
                $.scPlayer.stopAll();
                $('.album-controls').show();
                $('.player').empty();
                $('.player').append('<a href="http://api.soundcloud.com/tracks/' + $('.album-controls').data('album-audio') + '" class="sc-player">Player</a>');
                $('.sc-player').scPlayer();
            }
        }
    });

    $('.album-controls').click(function () {
        $('.album-controls').hide();
        $('.image-tag').click();
    });

    $('.cover').click(function() {
        $('.album-controls').hide();
    });

    var togglePlayButton = function() {
        $('.audio', $('.mfp-controls')).toggle();
    };

    $(document).bind('onPlayerPause.scPlayer', togglePlayButton)
                .bind('onPlayerPlay.scPlayer', togglePlayButton);
});
