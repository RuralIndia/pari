$(function () {
    var mapUrl = 'http://{s}.tile.cloudmade.com/ed59fdae04b74250b6cbf0bace768308/997/256/{z}/{x}/{y}.png',
        mapLayer = new L.TileLayer(mapUrl, {
            maxZoom: 7,
            attribution: '&copy; 2013 <a href="http://cloudmade.com/">CloudMade</a> – Map data ODbL 2013 <a href="http://www.openstreetmap.org/">OpenStreetMap.org</a> contributors – <a href="http://cloudmade.com/website-terms-conditions">Terms of Use</a>'
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