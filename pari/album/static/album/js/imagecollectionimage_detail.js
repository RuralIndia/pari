var Gallery ={

    init: function(){
            $('.popup-gallery').magnificPopup({
                delegate: '.mfp-image',
                type: 'image',
                tLoading: 'Loading image #%curr%...',
                closeOnContentClick: false,
                closeBtnInside: true,
                mainClass: 'mfp-album-popup',
                gallery: {
                    enabled: true,
                    navigateByImgClick: true,
                    preload: [0, 2]
                },
                image: {
                cursor: null,
                tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',

                markup: '<div class="mfp-figure">'+
                            '<div class="mfp-close"></div>'+
                            '<div class="mfp-img-holder">'+
                                '<div class="mfp-img"></div>'+
                            '</div>'+
                        '</div>'
                }
            });


          }
}

$(function(){
    Gallery.init();
});
