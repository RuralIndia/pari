var mapInterface = {
    init: function() {
        this.template = Handlebars.compile(this.source);
        this.populateLocations();
    },

    populateLocations: function() {
        $.get('/article/api/locations/?format=json', $.proxy(function(data) {
            this.data = data;
            $('#map').vectorMap({
                map: 'in_mill_en',
                regionStyle: {
                    initial: {
                        fill: 'grey'
                    }
                },
                backgroundColor: '#ffffff',
                markers: data,
                markerStyle: {
                    initial: {
                        fill: '#F8E23B',
                        stroke: '#383f47'
                    }
                },
                onMarkerClick: $.proxy(function(e, index){
                    this.onMarkerClick(e, index);
                }, this)
            });
        }, this));
    },

    onMarkerClick: function (e, index) {
        var id = this.data[index].id;
        $.get('/article/api/locations/' + id + '/article/?format=json', $.proxy(function(locationData) {
            var templateHtml= this.template(locationData);
            $("#side").html(templateHtml);
        }, this));

    },

    source: $("#article-template").html(),

    data: null
};


$(function(){
    mapInterface.init()
});