$(function () {
    var options = {center : new L.LatLng(21.7679,78.8718), zoom : 3 };
    
    var mapUrl = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png',
        osm = new L.TileLayer(mapUrl, {maxZoom: 3});
    
    var mapLayer = new L.TileLayer(mapUrl);
    
    var map = new L.Map('location-map', options).addLayer(mapLayer);
    map.locate({setView : true, maxZoom: 7});

    var source = $("#map-popup-template").html();
    var template = Handlebars.compile(source);

    $.get('/article/api/locations/?format=json', function(data) {
        $.each(data, function(i, location){
            var id = data[i].id;
            L.marker(location.latLng).addTo(map).on('click', function(e){
                $.get('/article/api/locations/' + id + '/article/?format=json', function(locationData) {
                    var templateHtml= template(locationData);
                    var popup = L.popup()
                                .setLatLng(e.target._latlng)
                                .setContent(templateHtml)
                                .openOn(map);
                    $("#side").html(templateHtml);
                });
            });
        })
    });

});