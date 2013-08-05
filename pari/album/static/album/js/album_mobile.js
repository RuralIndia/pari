var Album = {
    _popup: null,
    _sound: null,

    init: function () {
        this._initSoundCloudWidget();

        this._popup = $(".popup-gallery .mfp-image").photoSwipe({
            captionAndToolbarAutoHideDelay: 0,

            getImageCaption: function (el) {
                return el.getAttribute('title');
            },

            getImageMetaData: function (el) {
                return {
                    audio: el.getAttribute('data-audio')
                };
            },

            getToolbar: function () {
                return '<div class="ps-toolbar-close  ps-toolbar-item">' +
                            '<i class="icon-remove-circle"></i>' +
                        '</div>' +
                        '<div class="ps-toolbar-audio ps-toolbar-item">' +
                            '<i class="icon-play"></i>' +
                        '</div>' +
                        '<div class="ps-toolbar-previous ps-toolbar-item">' +
                            '<i class="icon-step-backward"></i>' +
                        '</div>' +
                        '<div class="ps-toolbar-next ps-toolbar-item">' +
                            '<i class="icon-step-forward"></i>' +
                        '</div>';
            }
        });

        this._popup.addEventHandler(Code.PhotoSwipe.EventTypes.onToolbarTap, $.proxy(this._onAudioClick, this));
        this._popup.addEventHandler(Code.PhotoSwipe.EventTypes.onHide, $.proxy(this._stopWidget, this));
        this._popup.addEventHandler(Code.PhotoSwipe.EventTypes.onDisplayImage, $.proxy(this._onLoadImage, this));

        $('.album-controls').on('click', $.proxy(this._startSlideshow, this));
    },

    _startSlideshow: function () {
        this._popup.show(0);

    },

    _onLoadImage: function (e) {
        var audio = this._popup.getCurrentImage().metaData.audio;
        this._reloadWidget(audio);
        this._initPlayAudioButton();
    },

    _onAudioClick: function (e) {
        var audioEl = Code.Util.DOM.find('div.ps-toolbar-audio')[0];
        if (e.tapTarget === audioEl || Code.Util.DOM.isChildOf(e.tapTarget, audioEl)) {
            this._toggleWidget();
        }
    },

    _initSoundCloudWidget: function () {
        SC.initialize({
            client_id: "d129911dd3c35ec537c30a06990bd902",
        });
    },

    _reloadWidget: function (audio, autoplay) {
        SC.stream("/tracks/" + audio, $.proxy(function (sound) {
            if (this._sound) {
                this._sound.stop();
            }
            this._sound = sound;
            if (autoplay) {
                this._playWidget();
            }
        }, this));
    },

    _playWidget: function () {
        this._sound.play({
            onfinish: this._initPlayAudioButton
        });
    },

    _toggleWidget: function () {
        this._toggleAudioButton();
        if (this._sound.playState === 0) {
            this._playWidget();
            return;
        }
        this._sound.togglePause();
    },

    _stopWidget: function () {
        this._sound.stop();
    },

    _toggleAudioButton: function () {
        var audioButton = $('.ps-toolbar-audio i');
        if (audioButton.hasClass('icon-play')) {
            this._initPauseAudioButton(audioButton);
        } else {
            this._initPlayAudioButton(audioButton);
        }
    },

    _initPlayAudioButton: function (audioButton) {
        audioButton = audioButton || $('.ps-toolbar-audio i');
        audioButton.removeClass('icon-pause');
        audioButton.addClass('icon-play');
    },

    _initPauseAudioButton: function (audioButton) {
        audioButton = audioButton || $('.ps-toolbar-audio i');
        audioButton.removeClass('icon-play');
        audioButton.addClass('icon-pause');
    }
};

$(function () {
    Album.init();
});
