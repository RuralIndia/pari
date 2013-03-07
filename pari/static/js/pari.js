$(function(){
    $('#subnav-wrapper').height($('#subnav').height());
    $('#subnav').affix({
        offset: {top: function() {
            var element = $('#subnav');
            if(!element.data('top')){
                element.data('top', element.position().top);
            }
            return element.data('top');
        }}
    });
});