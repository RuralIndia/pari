var Face = {
    init: function() {
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
                                '<h4 class="image-heading">'+ item.el.attr('data-title') + '</h4>' +
                                '<p class="image-district">' + item.el.attr('data-district') + '</p> <br />' +
                                '<p class="image-description">' + item.el.attr('data-description') + '</p>' +
                            '</div>'
                }, this),

                markup: '<div class="mfp-figure">'+
                            '<div class="mfp-close"></div>'+
                            '<div class="mfp-img-holder">'+
                                '<div class="mfp-img"></div>'+
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
                }, this),
                close: $.proxy(function () {
                    this._popup.removeData('slideshow');
                }, this)
            }
        });
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

            return false;
        }, this));

        $('.mfp-figure').on('click', function() {
            $('.mfp-container').removeClass('mfp-container-fullscreen');
        });
    }

}

$(function() {
    Face.init();
});

