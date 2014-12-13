$(function () {
    var mapUrl = 'http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg',
        mapLayer = new L.TileLayer(mapUrl, {
	    subdomains: '1234',
            maxZoom: 7,
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors. '
	    + 'Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>'
	    + '<img src="http://developer.mapquest.com/content/osm/mq_logo.png">'
        });
    
    var map = new L.Map('location-map', {}).addLayer(mapLayer);
    map.locate({setView : true, maxZoom: 7});

    var source = $("#map-popup-template").html();
    var template = Handlebars.compile(source);

    $.getJSON('/article/api/locations/?format=json', function(data) {
        $.each(data, function(i, location){
            var id = data[i].id;
            L.marker(location.latLng).addTo(map).on('click', function(e){
                $.getJSON('/article/api/locations/' + id + '/article/?format=json', function(locationData) {
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
