var Album = {
    init: function() {
        this._initSoundCloudWidget();
        this._initPopup();
        this._initControls();
    },

    _popup: null,
    _sound: null,

    _initPopup: function() {
        this._popup = $('.popup-gallery').magnificPopup({

            delegate: '.mfp-image',
            type: 'image',
            
            tLoading: 'Loading image #%curr%...',
            mainClass: 'mfp-album-popup',
            
            gallery: {
                enabled: true,
                navigateByImgClick: true,
                preload: [0, 2],
            },
                    
            image: {
                cursor: null,
                tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',

                titleSrc: $.proxy(function (item) {
                    var slideshow = this._popup.data('slideshow');
                    var icon = slideshow ? "pause" : "play";
                    return '<div>'+
                                '<h4 class="image-heading">'+ item.el.attr('data-photographer') + '</h4>' +
                                '<p class="image-date">' + item.el.attr('data-date') + '</p>' +
                                '<p class="image-location">' + item.el.attr('data-location') + '</p>' +
                                '<p class="image-location-description">' + item.el.attr('data-location-description') + '</p>' +
                                '<p class="image-caption" data-audio="' + item.el.attr('data-audio') + '">' + item.el.attr('title') + '</p>' +
                                '<div class="btn-toolbar">'+
                                    '<div class="btn-group">'+
                                        '<a class="btn btn-slideshow" href="#">Slideshow <i class="icon-' + icon + '"></i></a>'+
                                        '<a class="btn" href="' + item.el.attr('data-url') +'"><i class="icon-share"></i></a>'+
                                        '<a class="btn" href="' + item.el.attr('data-url') +'#comments"><i class="icon-comment-alt"></i></a>'+
                                        '<a class="btn btn-fullscreen" href="#"><i class="icon-fullscreen"></i></a>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'
                }, this),

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
                updateStatus: $.proxy(function () {
                    this._initImage();
                    this._initAudio();
                }, this),
                close: $.proxy(function () {
                    this._stopWidget();
                    this._popup.removeData('slideshow');
                }, this)
            }
        });
    },

    _initSoundCloudWidget: function() {
        SC.initialize({
            client_id: "d129911dd3c35ec537c30a06990bd902",
        });
    },

    _reloadWidget: function(audio, autoplay) {
        SC.stream("/tracks/" + audio, $.proxy(function(sound){
            if(this._sound){
                this._sound.stop();
            }
            this._sound = sound;
            if(autoplay){
                this._playWidget();
            }
        }, this));
    },

    _playWidget: function() {
        this._sound.play({
            onfinish: $.proxy(this._onSoundFinish, this)
        });
    },

    _toggleWidget: function() {
        this._togglePlayButton();
        if(this._sound.playState === 0) {
            this._playWidget();
            return;
        }
        this._sound.togglePause();
    },

    _updateSlideshowButtonIcon: function () {
        var slideshow = this._popup.data('slideshow');
        var slideshowButton = $('.btn-slideshow i');
        if(slideshow) { 
            slideshowButton.addClass('icon-pause');
            slideshowButton.removeClass('icon-play');
        } else {
            slideshowButton.addClass('icon-play');
            slideshowButton.removeClass('icon-pause');

        }

    },

    _stopWidget: function() {
        if(this._sound){
            this._sound.stop();
        }
    },

    _onSoundFinish: function() {
        var slideshow = this._popup.data('slideshow');
        if(slideshow) {
            var magnificPopup = $.magnificPopup.instance;
            magnificPopup.next();
            return;
        }
        this._initPlayButton();
    },

    _initControls: function() {
        $('.album-controls').click($.proxy(function () {
            this._popup.data('slideshow', 'true');
            this._popup.magnificPopup('open');
        }, this));
    },

    _initImage: function() {
        $('.btn-fullscreen').on('click', function() {
            $('.mfp-container').addClass('mfp-container-fullscreen');
            return false;
        });

        $('.btn-slideshow').on('click', $.proxy(function() {
            var slideshow = this._popup.data("slideshow");
            if(slideshow) {
                this._popup.removeData('slideshow');
            } else {
                this._popup.data('slideshow', 'true');
            }

            this._updateSlideshowButtonIcon();
            this._initAudio();

            return false;
        }, this));

        $('.mfp-figure').on('click', function() {
            $('.mfp-container').removeClass('mfp-container-fullscreen');
        });
    },

    _initAudio: function() {
        var audio = $('.mfp-title .image-caption').data('audio');
        var controls = $('.mfp-controls');
        var slideshow = this._popup.data('slideshow');

        if(audio && audio != "") {
            slideshow ? this._initPauseButton() : this._initPlayButton();

            controls.show();
            controls.off('click');
            controls.on('click', $.proxy(this._toggleWidget, this));

            this._reloadWidget(audio, slideshow);
        } else {
            controls.hide();
        }
    },

    _togglePlayButton: function() {
        $('.audio').toggle();
    },

    _initPlayButton: function(){
        $('.icon-play', '.mfp-controls').show();
        $('.icon-pause', '.mfp-controls').hide();
    },

    _initPauseButton: function(){
        $('.icon-play', '.mfp-controls').hide();
        $('.icon-pause', '.mfp-controls').show();
    }
}

$(function() {
    Album.init();
});
