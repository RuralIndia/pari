$(function () {
    var mapUrl = 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
        mapLayer = new L.TileLayer(mapUrl, {
            maxZoom: 7,
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        });
    
    var map = new L.Map('location-map', {}).addLayer(mapLayer);
    map.locate({setView : true, maxZoom: 7});

    var source = $("#map-popup-template").html();
    var template = Handlebars.compile(source);

    $.get('/article/api/locations/?format=json', function(data) {
        $.each(data, function(i, location){
            var id = data[i].id;
            L.marker(location.latLng).addTo(map).on('click', function(e){
                $.get('/article/api/locations/' + id + '/article/?format=json', function(locationData) {
                    var templateHtml= template(locationData);
                    var popup = L.popup({closeButton: false, offset: new L.Point(0, -20)})
                                .setLatLng(e.target._latlng)
                                .setContent(templateHtml)
                                .openOn(map);
                    $("#side").html(templateHtml);
                });
            });
        })
    });

});